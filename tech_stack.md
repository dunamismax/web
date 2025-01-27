# This setup leverages **Bun** as much as possible, along with a minimal but powerful ecosystem

## **Language & Runtime**

- **TypeScript (100%)**  
  - Compiled natively by Bun for both server and client code.
- **Bun**  
  - Serves as your main JavaScript/TypeScript runtime, bundler, and package manager.  
  - Built-in `.env` loading, built-in test runner (`bun test`), and fast `console` logging.

---

## **Server & Routing**

- **Hono**  
  - Lightweight, modern web framework (instead of Express).  
  - Middleware support for common tasks like parsing JSON, handling cookies, etc.  
  - A small, fast router well-suited for Bun.

---

## **Database & Queries**

- **Bun’s Built-in Postgres Client**  
  - Native Postgres driver for fast queries.
- **Drizzle**  
  - SQL toolkit/ORM layer on top of the Bun Postgres client.  
  - Handy for schema migrations, type-safe queries, and a more maintainable DB schema.

---

## **Front-End & Styles**

- **Pure HTML & Pico.css**  
  - Pico.css for minimal styling and clean defaults.  
  - Additional custom, vanilla CSS as needed.
- **HTMX**  
  - Enables interactive front-end features without heavy JavaScript frameworks.  
  - Leverages hypermedia-driven requests for partial page updates.

---

## **Environment & Configuration**

- **Bun’s `.env` Support**  
  - Load environment variables from `.env` files automatically.  
  - Access via `process.env.YOUR_VAR`.

---

## **Testing**

- **Bun’s Built-In Test Runner** (`bun test`)  
  - Jest-like syntax (`test()`, `expect()`) for unit and integration tests.  
  - Optionally integrate Drizzle migrations or a test database setup.

---

## **Logging**

- **Bun’s `console`**  
  - Native logging, optimized for performance.  
  - No external logger needed unless you want additional features (e.g., structured logs).

---

## **Summary**

This stack is lean yet capable. You use:

1. **Bun** as your core runtime, bundler, test runner, and environment manager.  
2. **Hono** for server routes and middleware.  
3. **Drizzle** + **Bun’s Postgres** for database queries and migrations.  
4. **pico.css**, custom CSS, **HTMX**, and vanilla HTML for the front end.  
5. **TypeScript** throughout, ensuring type safety from server to client code.  

Everything stays light, fast, and close to the metal of Bun’s native features.
