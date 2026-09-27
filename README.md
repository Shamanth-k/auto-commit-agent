# Daily Auto Commit Agent

A GitHub Actions automation that runs **without your computer being turned on**.

It selects predefined development tasks, applies them to another Git repository, validates the changes, creates Git commits, and remembers which tasks were already completed.

This README explains:

1. **How the project works**
2. **How to install it**
3. **How to connect it to your own GitHub repository**
4. **What you need to change if your repository has different files/code**
5. **How to run and troubleshoot it**

---

# 1. What is this project?

The project is a deterministic GitHub Actions automation.

You have two repositories:

```text
AUTOMATION REPOSITORY
        |
        | controls everything
        v
TARGET REPOSITORY
        |
        | receives the commits
        v
Your GitHub project
```

For example:

```text
yourname/auto-commit-agent
        |
        | creates commits in
        v
yourname/my-project
```

The automation repository contains the task system.

The target repository is the project that receives the changes.

---

# 2. How does it work?

Every day GitHub starts the workflow automatically.

The workflow does this:

```text
GitHub Scheduler
       |
       v
GitHub Actions Runner
       |
       v
Read task_pool.json
       |
       v
Read state.json
       |
       v
Select 3 unused tasks
       |
       v
Execute Task 1
       |
       v
Run validation/tests
       |
       v
Create Git commit
       |
       v
Execute Task 2
       |
       v
Run validation/tests
       |
       v
Create Git commit
       |
       v
Execute Task 3
       |
       v
Run validation/tests
       |
       v
Create Git commit
       |
       v
Update state.json
       |
       v
Push target repository
       |
       v
Push automation repository
```

Your computer is not involved.

GitHub provides the machine that runs the workflow.

---

# 3. Does it use AI?

No.

This project does not use:

- OpenAI
- ChatGPT
- Gemini
- Claude
- LLMs
- AI APIs

The tasks are predefined and deterministic.

The system does not ask an AI to decide what code to write.

---

# 4. What are the two repositories?

## Automation repository

Example:

```text
yourname/auto-commit-agent
```

This repository contains:

```text
app/
tasks/
.github/workflows/
```

It controls the automation.

Important files:

```text
tasks/task_pool.json
tasks/state.json
.github/workflows/daily-auto-commit.yml
app/daily_run.py
```

## Target repository

This is the repository that receives the changes.

Example:

```text
yourname/my-project
```

It can be your own GitHub project.

---

# 5. The most important thing to understand

The automation system is reusable, but the **tasks are not automatically compatible with every project**.

For example, if a task says:

```text
Add a function to src/calculator.py
```

your target repository must actually have the expected file and structure.

The current 108-task pool was created for the included:

```text
auto-commit-test-repo
```

Therefore:

```text
auto-commit-agent
        +
auto-commit-test-repo
```

is the currently tested combination.

If you want to use the system with **your own Git repository**, you have two options.

---

# 6. Option A — Use your own repository with compatible tasks

If your repository already has the files/functions expected by the tasks, you can point the automation to it.

You only need to change:

```text
TARGET_REPOSITORY
```

For example:

```text
TARGET_REPOSITORY = john123/my-project
```

However, the tasks must still be compatible with `my-project`.

---

# 7. Option B — Use your own repository and create your own tasks

This is the proper way to use the automation with a completely different project.

Suppose your repository is:

```text
john123/my-website
```

and it contains:

```text
src/
  components/
  utils/
  api/
tests/
README.md
```

You should create tasks that actually make sense for this project.

For example:

```text
Task 1
Add a test for the login helper

Task 2
Add documentation to the API helper

Task 3
Add validation for empty usernames

Task 4
Add a test for invalid email addresses

Task 5
Add a constant for the API timeout
```

The task pool should describe actions that the executors know how to perform.

---

# 8. How a task works internally

A task normally contains information similar to:

```json
{
  "id": 1,
  "title": "Add login validation test",
  "type": "testing",
  "action": "add_login_validation_test",
  "commit_message": "test: add login validation coverage"
}
```

The important fields are:

```text
id
title
type
action
commit_message
```

The workflow does not randomly invent code.

It reads the task and sends the `action` to the appropriate executor.

---

# 9. Executors

Executors contain the actual code that performs tasks.

The project contains executor categories such as:

```text
executors/
├── calculator.py
├── code_quality.py
├── config.py
├── documentation.py
├── file_utils.py
├── testing.py
├── text_utils.py
└── validator.py
```

For example:

```text
Task
  |
  | action:
  | add_login_validation_test
  v
Testing Executor
  |
  v
Modify target repository
  |
  v
Validator
  |
  v
Git commit
```

If you create tasks for a completely different project, you normally need to add or modify executors so those actions can actually be performed.

---

# 10. Task state

The file:

```text
tasks/state.json
```

keeps track of completed tasks.

Example:

```json
{
  "cycle": 1,
  "used_tasks": [
    1,
    5,
    8,
    14
  ],
  "total_tasks": 108
}
```

If task `5` is already in `used_tasks`, it will not be selected again during the current cycle.

With 108 tasks and 3 tasks per day:

```text
108 / 3 = 36 days
```

After all tasks are used, the system starts a new cycle.

---

# 11. Forking the project and `state.json`

When someone forks the automation repository, their fork also contains the current `tasks/state.json`. This is safe because the state file belongs to that fork and will be updated independently.

For example, if the original repository has already used 14 tasks, a new fork may initially contain those same 14 task IDs. The fork will then select from the remaining tasks and update its own `state.json`.

If the person wants to start a **completely fresh 108-task cycle**, they should reset `tasks/state.json` in their fork to:

```json
{
  "cycle": 1,
  "used_tasks": [],
  "total_tasks": 108
}
```

This gives the fork its own independent 36-day cycle at 3 tasks per day.

If they leave the existing state unchanged, the automation will simply continue from that state.

---

# 13. What happens if a task fails?

The system is designed to fail safely.

Example:

```text
Task starts
    |
    v
Task changes repository
    |
    v
Validation fails
    |
    v
Repository is restored
    |
    v
Task is NOT added to state.json
    |
    v
Workflow stops
```

This is important.

The system does not mark a failed task as completed.

---

# 13. Use it with your own GitHub repository

Now let's set up the project.

## Step 1 — Fork the automation repository

Click **Fork** on this repository.

You should get:

```text
YOUR_USERNAME/auto-commit-agent
```

---

## Step 2 — Choose your target repository

You can use:

```text
YOUR_USERNAME/my-project
```

or another repository that you own and can push to.

Make sure the automation has permission to push to it.

---

# 14. Create a GitHub Personal Access Token

The workflow needs permission to clone and push to your repositories.

Go to:

```text
GitHub
→ Settings
→ Developer settings
→ Personal access tokens
→ Fine-grained tokens
→ Generate new token
```

Choose:

```text
Repository access
→ Only select repositories
```

Select:

```text
YOUR_USERNAME/auto-commit-agent
YOUR_USERNAME/my-project
```

Give:

```text
Contents → Read and write
```

Create the token.

Copy it and keep it private.

---

# 15. Add the token to the automation repository

Open:

```text
YOUR_USERNAME/auto-commit-agent
```

Go to:

```text
Settings
→ Secrets and variables
→ Actions
→ Secrets
→ New repository secret
```

Create:

```text
Name:
AUTO_COMMIT_PAT
```

Value:

```text
YOUR_PERSONAL_ACCESS_TOKEN
```

Save it.

Never put the token directly in the YAML file.

---

# 16. Tell the automation which repository to use

Go to:

```text
Settings
→ Secrets and variables
→ Actions
→ Variables
→ New repository variable
```

Create:

```text
Name:
TARGET_REPOSITORY
```

Value:

```text
YOUR_USERNAME/my-project
```

For example:

```text
Shamanth-k/my-project
```

Do NOT use:

```text
https://github.com/Shamanth-k/my-project
```

Use only:

```text
Shamanth-k/my-project
```

---

# 17. Set the commit name

Create another variable:

```text
Name:
COMMIT_NAME
```

Value:

```text
Your Name
```

Example:

```text
Shamanth Krishna V R
```

This is the name that Git will use for the automated commits.

---

# 18. Set the commit email

Create:

```text
Name:
COMMIT_EMAIL
```

Value:

```text
Your GitHub no-reply email
```

You can find your email at:

```text
GitHub
→ Settings
→ Emails
```

It may look like:

```text
12345678+username@users.noreply.github.com
```

Use the exact address shown by GitHub.

---

# 19. Your final GitHub settings

Your automation repository should have:

## Secrets

```text
AUTO_COMMIT_PAT
```

## Variables

```text
COMMIT_NAME
COMMIT_EMAIL
TARGET_REPOSITORY
```

Example:

```text
COMMIT_NAME
Shamanth Krishna V R

COMMIT_EMAIL
156513586+Shamanth-k@users.noreply.github.com

TARGET_REPOSITORY
Shamanth-k/my-project
```

---

# 20. Check the workflow

The important parts of the workflow are:

```yaml
- name: Clone target repository
  env:
    TARGET_TOKEN: ${{ secrets.AUTO_COMMIT_PAT }}
  run: |
    git clone "https://x-access-token:${TARGET_TOKEN}@github.com/${{ vars.TARGET_REPOSITORY }}.git" "$RUNNER_TEMP/target"
```

This means:

```text
TARGET_REPOSITORY
        |
        v
GitHub clones your project
```

Then:

```yaml
- name: Configure target Git
  working-directory: ${{ runner.temp }}/target
  run: |
    git config user.name "${{ vars.COMMIT_NAME }}"
    git config user.email "${{ vars.COMMIT_EMAIL }}"
```

This controls who appears as the Git commit author.

---

# 21. Run it manually first

Go to:

```text
Actions
→ Daily Auto Commit
→ Run workflow
```

Run it manually.

Do not wait for the scheduled run for your first test.

---

# 22. Check the result

If successful, open your target repository:

```text
YOUR_USERNAME/my-project
```

Go to:

```text
Commits
```

You should see the commits created by the automation.

Also check:

```text
YOUR_USERNAME/auto-commit-agent
```

You should see the state update commit.

---

# 23. Daily schedule

The default workflow schedule is:

```text
00:30 UTC
06:00 IST
```

After the workflow is enabled, GitHub runs it automatically.

Your computer can be:

```text
OFF
```

VS Code can be:

```text
CLOSED
```

PowerShell can be:

```text
CLOSED
```

The workflow still runs because GitHub provides the runner.

---

# 24. What you need to change for a completely new project

If you want to use this system with a repository that is structurally different from `auto-commit-test-repo`, changing only:

```text
TARGET_REPOSITORY
```

is **not enough**.

You should normally update:

```text
1. tasks/task_pool.json
2. app/executors/
3. validation logic
4. tests
```

The reason is simple:

```text
New repository
      |
      v
Different files
      |
      v
Different functions
      |
      v
Different tasks required
      |
      v
Different executors may be required
```

For example, a task that modifies:

```text
src/calculator.py
```

will fail if your new project has no such file.

---

# 25. Example: using your own project

Suppose your repository is:

```text
john123/weather-api
```

and it contains:

```text
src/
  api.py
  weather.py
tests/
  test_weather.py
README.md
```

You could create tasks such as:

```text
1. Add a weather API timeout test
2. Add documentation to weather.py
3. Add invalid city input validation
4. Add a test for empty API responses
5. Add a constant for API timeout
```

Then create executors that know how to perform those actions.

After that, configure:

```text
TARGET_REPOSITORY
=
john123/weather-api
```

The automation repository can then run those tasks against the new project.

---

# 26. Security

The repository can be public.

These are okay to store as normal repository variables:

```text
COMMIT_NAME
COMMIT_EMAIL
TARGET_REPOSITORY
```

This must remain a GitHub Secret:

```text
AUTO_COMMIT_PAT
```

Never commit a token such as:

```text
github_pat_...
```

to the repository.

If a token is accidentally published, revoke it immediately and create a new one.

---

# 27. Common errors

## `Repository not found`

Check:

```text
TARGET_REPOSITORY
```

It must be:

```text
username/repository
```

not a full URL.

---

## `Authentication failed`

Check that:

- The PAT is still valid.
- The PAT has access to the target repository.
- `Contents → Read and write` is enabled.
- `AUTO_COMMIT_PAT` is stored under **Secrets**, not Variables.

---

## `Function already exists`

Example:

```text
Function already exists: build_config
```

This normally means the selected task expects to create something that is already present in the target repository.

Check:

```text
tasks/state.json
```

and the target repository history before changing anything.

---

## `Task produced no changes`

This means the executor ran but did not produce a Git change.

The task may already have been completed or may not match the target project's current state.

---

# 28. Project structure

```text
auto-commit-agent/
│
├── .github/
│   └── workflows/
│       └── daily-auto-commit.yml
│
├── app/
│   ├── daily_run.py
│   ├── executors/
│   ├── git/
│   ├── task_manager/
│   └── validation/
│
├── tasks/
│   ├── task_pool.json
│   └── state.json
│
├── README.md
└── .gitignore
```

---

# 29. Simple explanation

If you are completely new to the project, remember this:

```text
AUTO-COMMIT-AGENT
       |
       | "What should I do?"
       v
TASK POOL
       |
       | "Which tasks are already done?"
       v
STATE.JSON
       |
       | "Perform this task."
       v
EXECUTOR
       |
       | "Did it work?"
       v
VALIDATOR
       |
       | "Yes."
       v
GIT COMMIT
       |
       v
YOUR REPOSITORY
```

The automation repository is the **brain/controller**.

Your own Git repository is the **target**.

The task pool tells the system what to do.

The executors perform the tasks.

The validator checks the result.

Git creates the commits.

`state.json` remembers what has already been done.

---

# 30. Final checklist

Before running:

- [ ] Forked `auto-commit-agent`
- [ ] Have a target GitHub repository
- [ ] Created a fine-grained PAT
- [ ] PAT has `Contents → Read and write`
- [ ] PAT can access both repositories
- [ ] Added `AUTO_COMMIT_PAT` as a Secret
- [ ] Added `TARGET_REPOSITORY` as a Variable
- [ ] Added `COMMIT_NAME` as a Variable
- [ ] Added `COMMIT_EMAIL` as a Variable
- [ ] Checked that the task pool matches the target repository
- [ ] Enabled GitHub Actions
- [ ] Ran the workflow manually
- [ ] Confirmed the target repository received commits
- [ ] Confirmed `tasks/state.json` was updated

Once the first manual run succeeds, GitHub can continue running the workflow automatically every day.
