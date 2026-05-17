# Postman Collection Documentation

## Collection Name

JSONPlaceholder Posts API Automation

## Purpose

This Postman collection validates basic API flows for the JSONPlaceholder `/posts` resource. It covers read, create, and delete operations using automated Postman test scripts.

Base API:

```text
https://jsonplaceholder.typicode.com
```

Collection file:

```text
JSONPlaceholder Posts API Automation.postman_collection.json
```

## Collection Variables

| Variable | Value | Purpose |
|---|---:|---|
| `baseUrl` | `https://jsonplaceholder.typicode.com` | Base URL for all API requests |
| `postIdToDelete` | `1` | Post ID used by the DELETE request |
| `createdPostId` | Empty by default | Stores the ID returned by the POST request |

## API Requests

### 1. GET /posts - Validate Status 200

**Method**

```text
GET
```

**Endpoint**

```text
{{baseUrl}}/posts
```

**Purpose**

Fetches all posts from JSONPlaceholder and validates that the API is reachable and returns a valid posts array.

**Expected Status Code**

```text
200 OK
```

**Automated Validations**

- Response status code is `200`.
- Response body is a non-empty array.
- First post contains the required fields:
  - `userId`
  - `id`
  - `title`
  - `body`

**Sample Test Script**

```javascript
pm.test('Status code is 200', function () {
    pm.response.to.have.status(200);
});

pm.test('Response is a non-empty array of posts', function () {
    const posts = pm.response.json();
    pm.expect(posts).to.be.an('array').that.is.not.empty;
    const requiredKeys = ['userId', 'id', 'title', 'body'];
    requiredKeys.forEach((key) => {
        pm.expect(posts[0]).to.have.property(key);
    });
});
```

## 2. POST /posts - Create Post And Validate Echoed Body

**Method**

```text
POST
```

**Endpoint**

```text
{{baseUrl}}/posts
```

**Headers**

| Key | Value |
|---|---|
| `Content-Type` | `application/json` |

**Request Body**

```json
{
  "title": "api automation title",
  "body": "api automation body",
  "userId": 1
}
```

**Purpose**

Creates a new post and validates that the API response returns the same `title`, `body`, and `userId` sent in the request.

JSONPlaceholder is a fake online REST API, so this request simulates creation and returns a successful response, but it does not permanently save the post on the server.

**Expected Status Code**

```text
201 Created
```

**Automated Validations**

- Response status code is `201`.
- Response `title` matches request `title`.
- Response `body` matches request `body`.
- Response `userId` matches request `userId`.
- Response contains an `id`.
- Returned `id` is stored in collection variable `createdPostId`.

**Sample Test Script**

```javascript
pm.test('Status code is 201', function () {
    pm.response.to.have.status(201);
});

pm.test('Response contains same title and body as request', function () {
    const requestBody = JSON.parse(pm.request.body.raw);
    const responseBody = pm.response.json();
    pm.expect(responseBody.title).to.eql(requestBody.title);
    pm.expect(responseBody.body).to.eql(requestBody.body);
    pm.expect(responseBody.userId).to.eql(requestBody.userId);
    pm.expect(responseBody).to.have.property('id');
    pm.collectionVariables.set('createdPostId', responseBody.id);
});
```

## 3. DELETE /posts/{id} - Validate Status 200 Or 204

**Method**

```text
DELETE
```

**Endpoint**

```text
{{baseUrl}}/posts/{{postIdToDelete}}
```

**Purpose**

Deletes a post by ID and validates that the API returns a successful delete response.

For this collection, `postIdToDelete` defaults to `1`.

JSONPlaceholder simulates delete behavior. The response indicates success, but the resource is not permanently deleted.

**Expected Status Code**

```text
200 OK
```

or

```text
204 No Content
```

**Automated Validations**

- Response status code is either `200` or `204`.

**Sample Test Script**

```javascript
pm.test('Status code is 200 or 204', function () {
    pm.expect([200, 204]).to.include(pm.response.code);
});
```

## Execution Steps In Postman

1. Open Postman.
2. Click **Import**.
3. Select the collection JSON file:

```text
JSONPlaceholder Posts API Automation.postman_collection.json
```

4. Confirm the collection variable `baseUrl` is set to:

```text
https://jsonplaceholder.typicode.com
```

5. Open the collection.
6. Click **Run Collection**.
7. Select all three requests:
   - `GET /posts - validate status 200`
   - `POST /posts - create post and validate echoed body`
   - `DELETE /posts/{id} - validate status 200 or 204`
8. Click **Run**.

## Expected Collection Run Result

All requests should pass their Postman test scripts.

Expected summary:

```text
GET /posts       - Passed
POST /posts      - Passed
DELETE /posts/1  - Passed
```

## Notes

- JSONPlaceholder is a mock REST API service.
- POST and DELETE requests return successful responses but do not permanently modify server data.
- This collection is suitable for API automation practice, smoke testing, and demonstrating Postman test script usage.
