# Project & Folder Structure, Future Scalability, and Next-Step AI Prompts

Below is a comprehensive **project structure** (in its current minimal form) along with a suggested **expanded structure** for a larger-scale project. Following that, you’ll find a series of **sequential prompts** that you can feed to an AI LLM to iteratively enhance the site step by step.

---

## Current Minimal Structure

```plaintext
my-blog/
 ┣ drizzle/
 ┃ ┗ migrations/         # Drizzle migration files (generated)
 ┣ src/
 ┃ ┣ schema/
 ┃ ┃ ┗ posts.ts          # Drizzle schema for 'posts' table
 ┃ ┣ db.ts               # Database connection (Bun + Drizzle)
 ┃ ┗ app.ts              # Hono app setup and routes
 ┣ .env                  # Environment variables (DATABASE_URL, etc.)
 ┣ drizzle.config.ts     # Drizzle config for migrations
 ┣ tsconfig.json         # TypeScript configuration
 ┣ bun.toml              # Bun-specific configuration (dependencies, scripts)
 ┗ README.md             # Project documentation/instructions
```

### Brief Description of Each Key File

- **drizzle.config.ts**: Configures Drizzle migrations (points to schema, output directory, driver, etc.).  
- **src/schema/posts.ts**: Defines the `posts` table using Drizzle’s `pg-core`.  
- **src/db.ts**: Initializes the Postgres connection pool and Drizzle client.  
- **src/app.ts**: Creates the Hono server, sets up routes for `/`, `/blog`, `/about`, `/contact`.  
- **.env**: Stores environment variables, e.g., `DATABASE_URL`.  
- **drizzle/migrations/**: Contains auto-generated migration files that reflect your schema changes.  
- **tsconfig.json**: TypeScript compiler settings.  
- **bun.toml**: Bun configuration (scripts, dev server, etc.).  
- **README.md**: Project usage instructions.

---

## Future, Expanded Project Structure (Theoretical Larger Scale)

As your codebase grows, you may want to reorganize and modularize. Here’s a **potential future layout**:

```plaintext
my-blog/
 ┣ drizzle/
 ┃ ┗ migrations/                # Migration files
 ┣ src/
 ┃ ┣ config/
 ┃ ┃ ┗ index.ts                 # App-wide config, environment logic
 ┃ ┣ db.ts                      # Database connection (Drizzle + Bun)
 ┃ ┣ schema/
 ┃ ┃ ┣ posts.ts                 # Table definitions for 'posts'
 ┃ ┃ ┗ users.ts                 # Future: Table definitions for 'users'
 ┃ ┣ routes/
 ┃ ┃ ┣ blog/
 ┃ ┃ ┃ ┣ blog.controller.ts     # Business logic for blog posts
 ┃ ┃ ┃ ┣ blog.routes.ts         # Hono routes for blog
 ┃ ┃ ┃ ┗ blog.types.ts          # Type definitions & interfaces
 ┃ ┃ ┣ contact/
 ┃ ┃ ┃ ┣ contact.controller.ts  # Business logic for contact
 ┃ ┃ ┃ ┗ contact.routes.ts      # Hono routes for contact
 ┃ ┃ ┣ about/
 ┃ ┃ ┃ ┗ about.routes.ts        # Hono routes for about
 ┃ ┃ ┗ index.ts                 # Aggregates/exports all route modules
 ┃ ┣ middleware/
 ┃ ┃ ┗ index.ts                 # Hono middlewares (logger, error handling, etc.)
 ┃ ┣ services/
 ┃ ┃ ┗ mail.service.ts          # Example: Email sending logic
 ┃ ┣ utils/
 ┃ ┃ ┗ validations.ts           # Common validation functions
 ┃ ┗ app.ts                     # Main Hono app configuration (imports routes, middleware)
 ┣ tests/
 ┃ ┣ integration/
 ┃ ┃ ┗ blog.test.ts            # Integration tests for blog routes
 ┃ ┣ unit/
 ┃ ┃ ┣ db.test.ts              # Unit tests for database queries
 ┃ ┃ ┗ validations.test.ts     # Unit tests for utility validations
 ┣ .env                         # Environment variables
 ┣ drizzle.config.ts            # Drizzle config
 ┣ tsconfig.json                # TypeScript config
 ┣ bun.toml                     # Bun config
 ┗ README.md                    # Documentation
```

### Explanation of Expanded Structure

- **config/**: Central place for environment-based settings, feature toggles, or shared constants.  
- **schema/**: Separate each table or model in its own file.  
- **routes/**: Group routes by feature or domain (e.g., `blog`, `about`, `contact`). Each feature can have its own “controller” and “routes” for clearer separation of concerns.  
- **middleware/**: Hono or custom middleware modules (e.g., logging, authorization, error-handling).  
- **services/**: Feature-agnostic business logic, e.g., email sending, file uploads, external API calls.  
- **utils/**: Reusable functions (validation, formatting, etc.).  
- **tests/**: Organized into `integration` vs. `unit` tests for clarity.  

This structure should remain **flexible**, but it demonstrates how you might scale beyond a single-file approach when your application logic grows more complex.

---

## Ordered Prompts for Next Steps

Below is a list of **prompts** you can use in sequence, from **basic** to **advanced**, to iteratively improve this site. Each prompt is written as if you were instructing an AI LLM. You could copy/paste these **in order** to systematically enhance your blog.

1. **Prompt 1**:  
   > “Refactor the existing codebase to move all route logic for the `/blog` endpoint into its own separate `blog.routes.ts` file under a new `routes/blog/` folder, and import that file in the main `app.ts`. Maintain TypeScript types throughout and ensure that Drizzle queries and response handling remain consistent.”

2. **Prompt 2**:  
   > “Add a new route in `blog.routes.ts` for creating new blog posts. This route should accept `title` and `content` from the request body, insert a new entry into the `posts` table using Drizzle, and return a success message along with the newly created post ID. Use Hono’s built-in JSON middleware to parse request bodies.”

3. **Prompt 3**:  
   > “Implement client-side interactivity on the blog page using HTMX, allowing new blog posts to be created without a full page reload. Modify the `/blog` route to return a small HTML snippet for newly created posts, and update the blog listing in the DOM dynamically when a new post is submitted.”

4. **Prompt 4**:  
   > “Introduce basic unit tests with `bun test` for the blog routes. Test the creation of new blog posts to ensure the route inserts data correctly into the database. Use `describe()` blocks to separate test suites, and mock/stub the database connection if needed.”

5. **Prompt 5**:  
   > “Implement an error handling middleware in Hono that catches any thrown errors or unhandled promise rejections, logs them, and returns a standardized JSON error object with an appropriate HTTP status code. Place this middleware near the top of the middleware chain to capture all errors.”

6. **Prompt 6**:  
   > “Add input validation and sanitization to the blog post creation route. Use a shared validation utility or library (e.g., Zod or a custom function) in the `utils/validations.ts` file. Ensure that no empty titles are allowed, the maximum title length is 255 characters, and the content must not exceed 10,000 characters.”

7. **Prompt 7**:  
   > “Expand the database schema to include a `slug` column in the `posts` table and update the blog creation route to auto-generate this slug from the title. Use a slug generation library or a simple utility function, ensuring uniqueness by appending an increment if a collision occurs.”

8. **Prompt 8**:  
   > “Refactor the project into a more modular structure to accommodate future growth: create a `routes/` folder, a `services/` folder for business logic, and a `middleware/` folder. Update all imports to reference the new locations.”

9. **Prompt 9**:  
   > “Enhance the front-end styling using Pico.css classes and your Nord color overrides. Ensure that headings, paragraphs, and navigation elements stand out more distinctly. Keep the Fira Code font usage consistent across all text elements.”

10. **Prompt 10**:  
    > “Set up pagination for the blog listings so that if more than 10 posts exist, the `/blog` page automatically shows only the first 10, and includes `Next` / `Previous` links to navigate through pages. Implement it using server-side logic in Hono and minimal HTMX for partial page updates.”

11. **Prompt 11**:  
    > “Build integration tests for your pagination logic to verify that the correct number of items displays per page and that navigation links fetch the expected posts. Use `bun test` and create a dedicated test file in the `tests/integration/blog.test.ts` path.”

12. **Prompt 12**:  
    > “Add a contact form on the `/contact` page that uses HTMX for submission, performing basic field validation on the server side. Display either a success message or validation errors without requiring a full page reload.”

13. **Prompt 13**:  
    > “Refactor your error messaging to use a shared utility function so that consistent error responses can be reused throughout the application, including blog routes and the contact form. Document this utility in the `utils/` folder.”

14. **Prompt 14**:  
    > “Implement a testing strategy for your contact form. Write unit tests for your validation logic and an integration test that submits sample form data to the contact route to ensure correct behavior.”

15. **Prompt 15**:  
    > “Add a global configuration system under `src/config/` that can handle environment-specific values (e.g., development vs. production) for things like logging verbosity, external service URLs, or feature toggles. Update the project to read from this config instead of using hardcoded values.”

16. **Prompt 16**:  
    > “Optimize performance by adding an index to the `title` column in the `posts` table if you plan to query by title frequently. Use Drizzle’s migration mechanism to create a new migration that adds this index, then run the migration and confirm it works in your local environment.”

---

### How to Use These Prompts

1. **Copy** the first prompt verbatim and paste it into your AI LLM (e.g., ChatGPT, etc.).  
2. Once you have the revised code or instructions, **apply** the changes to your codebase.  
3. Proceed to the **next prompt** and repeat.  

By following these prompts in order, you’ll systematically **refactor**, **improve**, and **scale** your codebase. Each step focuses on best practices for maintainability, type safety, test coverage, and user experience.

---
