# Club Booking SaaS Platform API
Multi-tenant booking engine for Players and Club Owners.

## Version: 2.0.0

### Servers

| URL | Description |
| --- | ----------- |
| http://127.0.0.1:5000/api/v1 | Local Flask Development Server |

### Available authorizations
#### bearerAuth (HTTP, bearer)
Bearer format: JWT

---

### [POST] /auth/register
**Register a new user**

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"name"**: string, **"email"**: string (email), **"password"**: password, **"role"**: string, <br>**Available values:** "player", "owner" }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | User registered |

### [POST] /auth/login
**Authenticate user (JWT)**

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"email"**: string, **"password"**: string }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful login returns JWT access_token |

### [GET] /clubs
**List all active clubs (Player Discovery)**

#### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Array of available clubs | **application/json**: [ [Club](#club-schema) ]<br> |

### [POST] /clubs
**Register a new Club (Owner Only)**

Requires 'owner' role. The JWT identity is automatically set as the owner_id.

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"name"**: string, **"address"**: string, **"operating_hours"**: [OperatingHours](#operatinghours-schema) }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Club created successfully |

### [PUT] /clubs/{clubId}
**Update Club settings & availability (Owner Only)**

Verifies JWT identity matches Club's owner_id.

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| clubId | path |  | Yes | integer |

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"operating_hours"**: [OperatingHours](#operatinghours-schema) }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Club settings updated |

### [POST] /clubs/{clubId}/courts
**Add a court to a club (Owner Only)**

Verifies JWT identity matches Club's owner_id.

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| clubId | path |  | Yes | integer |

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"name"**: string, **"operating_hours_override"**: [OperatingHours](#operatinghours-schema) }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Court added to club |

### [GET] /clubs/{clubId}/availability
**Get court availability for a specific club and date**

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| clubId | path |  | Yes | integer |
| date | query |  | Yes | date |

#### Responses

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Returns matrix of courts and slots generated dynamically based on operating hours. | **application/json**: [ { **"court_id"**: integer, **"court_name"**: string, **"slots"**: [ { **"start_time"**: string, **"end_time"**: string, **"status"**: string, <br>**Available values:** "available", "booked", "blocked" } ] } ]<br> |

### [POST] /bookings
**Player books a slot**

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"court_id"**: integer, **"booking_date"**: date, **"start_time"**: string, **"end_time"**: string }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Booking successful |
| 409 | Race condition (slot overlapping via GiST constraint) |

### [PATCH] /bookings/{bookingId}/release
**Release an active slot to the public (Player)**

#### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ------ |
| bookingId | path |  | Yes | integer |

#### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Slot released (soft-delete) |

### [POST] /admin/overrides
**Force override a player's slot (Owner Only)**

Verifies JWT identity matches the owner of the club housing the court.

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"booking_id"**: integer, **"reason"**: string }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Override initiated |

### [POST] /admin/blocks
**Block a court for maintenance/tournament (Owner Only)**

Verifies JWT identity matches the owner of the club housing the court.

#### Request Body

| Required | Schema |
| -------- | ------ |
|  Yes | **application/json**: { **"court_id"**: integer, **"start_date"**: date, **"end_date"**: date, **"title"**: string }<br> |

#### Responses

| Code | Description |
| ---- | ----------- |
| 201 | Court blocked |

---
### Schemas

#### ErrorResponse Schema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| code | string |  | No |
| message | string |  | No |

#### OperatingHours Schema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| open_time | string | HH:MM format<br>*Example:* `"06:00"` | No |
| close_time | string | HH:MM format<br>*Example:* `"22:00"` | No |
| slot_duration_minutes | integer | Granularity of bookable slots<br>*Example:* `60` | No |

#### Club Schema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| name | string |  | No |
| address | string |  | No |
| owner_id | integer |  | No |
| operating_hours | [OperatingHours](#operatinghours-schema) |  | No |

#### Court Schema

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| id | integer |  | No |
| club_id | integer |  | No |
| name | string |  | No |
| is_active | boolean |  | No |
| operating_hours_override | [OperatingHours](#operatinghours-schema) |  | No |
