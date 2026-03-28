
# GitHub Copilot Commit Message Instructions

## Best Practices for VS Code

### Format
- **Format**: `<type>(<scope>): <subject>`
- **Limit subject line** to 50 characters
- **Use imperative mood**: "add" not "added" or "adds"

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build, dependencies, or tooling changes

### Guidelines
1. **Be specific**: Describe *what* and *why*, not just *what*
2. **Keep it concise**: Avoid unnecessary details in the subject
3. **Add body** (optional): Separate from subject with blank line for context
4. **Reference issues**: Use `Fixes #123` or `Closes #456`
5. **Limit line length** keep it very short not exeeding 50 characters

### Example
```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh to improve user session management.
Reduces session timeouts and improves UX.

Fixes #234
```

### VS Code Tips
- Use Copilot to suggest messages based on staged changes
- Review suggestions before committing
- Align with your project's contribution guidelines
