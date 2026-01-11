# 🤝 Contributing Guide

Thank you for your interest in contributing to the Claude Skills Template!

## How to Contribute

### Report Issues
- Use GitHub's issue system
- Clearly describe the problem or suggestion
- Include examples when possible

### Improve Documentation
- Fix typos
- Improve explanation clarity
- Add useful examples
- Translate to other languages

### Add New Skills
1. Create a new directory in `skills/`
2. Follow the standard structure:
   - `SKILL.md` with YAML frontmatter
   - `scripts/` (optional) for helpers
3. Document clearly:
   - Skill purpose
   - Methodology it applies
   - Usage examples
   - How it integrates with other skills

### Improve Existing Skills
- Refine methodologies
- Add more examples
- Improve helper scripts
- Optimize for better performance

### Share Examples
- Add real use cases
- Document solved problems
- Share discovered best practices

## Quality Standards

### Documentation
- Use Markdown correctly
- Include practical examples
- Maintain style consistency
- Update indexes when adding content

### Code
- Follow PEP 8 for Python
- Comment complex code
- Include docstrings
- Keep functions small and focused

### Skills
- Correct YAML frontmatter format
- Clear and concise description
- Well-defined methodology
- Relevant examples

## Contribution Process

1. **Fork** the repository
2. **Create a branch** for your contribution
   ```bash
   git checkout -b feature/my-contribution
   ```
3. **Make your changes** following standards
4. **Test** that everything works correctly
5. **Commit** with descriptive messages
   ```bash
   git commit -m "feat: add new testing skill"
   ```
6. **Push** to your fork
   ```bash
   git push origin feature/my-contribution
   ```
7. **Open a Pull Request** with clear description

## Commit Conventions

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New functionality
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, missing semicolon, etc.
- `refactor:` Code refactoring
- `test:` Add or modify tests
- `chore:` Build changes, dependencies, etc.

## Pull Request Structure

### Title
- Descriptive and clear
- Prefix with type (feat, fix, docs, etc.)

### Description
- What changes?
- Why is it necessary?
- How does it work?
- Usage examples?

### Checklist
- [ ] Code/documentation updated
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] Examples updated (if applicable)

## Priority Contribution Areas

### High Priority
- Improve documentation of existing skills
- Add more usage examples
- Optimize skill methodologies

### Medium Priority
- Create new complementary skills
- Improve helper scripts
- Add specific use cases

### Low Priority
- Translations
- Style improvements
- Minor optimizations

## Frequently Asked Questions

### Do I need previous experience?
No, any contribution is welcome. If you have questions, open an issue to discuss.

### How do I know if my contribution is valuable?
All contributions are valuable. Even small documentation improvements help.

### Can I contribute skills from other projects?
Yes, as long as you respect licenses and give appropriate credit.

### Is there a code of conduct?
Yes, maintain a respectful and collaborative environment.

## Useful Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Claude Skills Best Practices](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Awesome Claude Skills](https://github.com/VoltAgent/awesome-claude-skills) - Inspiration

## Contact

- Open an issue for questions
- Use discussions for general ideas
- Pull requests for concrete contributions

---

**Thank you for contributing!** Every contribution makes this template better for the entire community. 🎉
