# Overview
A simple multi-threaded web server built using Python's socket programming. This server can handle multiple simultaneous HTTP requests, serve static HTML files and images, support 301 redirects, and display a custom 404 error page for non-existent resources.

## Features
- **Static File Serving:** Serves HTML pages and images stored locally.
- **Custom 404 Page:** Displays a custom 404 error page when a requested resource is not found.
- **301 Redirects:** Implements a hardcoded 301 redirect from `/page1.html` to `/page2.html`.
- **Multi-Threading:** Supports multiple client requests simultaneously using Python's threading module.
- **Local Testing:** Runs on `localhost` at port `8080`, making it easy to test on your local machine.

## Files Included
- **`index.html`:** Main webpage with an embedded image.
- **`page2.html`:** The destination page for the hardcoded 301 redirect.
- **`404.html`:** Custom 404 error page displayed when a resource is not found.
- **`don.jpg`:** Image file displayed on the `index.html` page.
- **`server.py`:** The Python script implementing the multi-threaded web server.

## How to Run
1. Make sure you have Python 3.x installed on your system.
2. Clone the repository.
3. Open a terminal or command prompt and navigate to the `multithread-webserver` directory:
    ```bash
    cd multithread-webserver
    ```
4. Run the server script:
    ```bash
    python server.py
    ```
5. The server will start and listen for incoming connections on `127.0.0.1:8080`.

## Testing the Server
1. Open a web browser and navigate to:
    - `http://localhost:8080/` to view the `index.html` page with the embedded image (`don.jpg`).
    - `http://localhost:8080/page1.html` to trigger the 301 redirect to `page2.html`.
    - `http://localhost:8080/nonexistent.html` to see the custom 404 error page.

## Known Bugs and Limitations
- **File Type Limitations:** Currently, the server only serves HTML and JPEG files. Other file types may not be handled correctly.
- **Thread Limit:** The server creates a new thread for each request. It may experience slowdowns if handling a large number of simultaneous requests due to system resource limitations.
- **Hardcoded Redirect:** The 301 redirect is hardcoded for `/page1.html` to `/page2.html`. Additional redirects would require modifying the server code.

## Future Improvements
- Add support for more file types (e.g., PNG, CSS, JavaScript).
- Implement dynamic 301 redirects based on server configurations.
- Enhance error handling and logging mechanisms for better debugging.

## License
This project is open-source and available for use under the [MIT License](LICENSE).

