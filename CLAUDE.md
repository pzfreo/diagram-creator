# Claude Code Instructions for Overstand

## Project Overview
Overstand is a parametric CAD tool for lutherie - generating precise neck templates for arched instruments. It has a Python backend (geometry engine) and a web frontend (PWA).

## Development Workflow

### Always Use Feature Branches and PRs
- Never commit directly to main
- Create a feature branch for each change: `claude/descriptive-name-XXXXX`
- Push changes and create a PR for review
- Include a clear PR description with summary and test plan

### Testing Requirements
**Before committing any changes:**
1. Run Python tests: `pytest tests/`
2. Run JavaScript tests: `npm test`
3. If you modify code, ensure existing tests pass
4. Write tests for new functionality - aim for test coverage of new code paths

### Code Quality
- Follow existing code patterns and style in the codebase
- Don't over-engineer - make minimal changes needed for the task
- Don't add features beyond what was requested
- Keep functions focused and single-purpose
- Handle errors appropriately but don't add defensive code for impossible cases

### Commit Practices
- Write clear, descriptive commit messages explaining "why" not just "what"
- Make atomic commits - one logical change per commit
- Run tests before committing

## Commands Reference

```bash
# Python tests
pytest tests/
pytest tests/test_geometry_engine.py -v  # specific file

# JavaScript tests
npm test
npm run test:watch    # watch mode
npm run test:coverage # with coverage

# Build for production
./scripts/build.sh

# Local development
# Open web/index.html in browser (or use a local server)
```

## Project Structure
- `src/` - Python geometry engine modules
- `web/` - Frontend (HTML, CSS, JS)
- `tests/` - Python test files
- `presets/` - Instrument preset JSON files
- `scripts/` - Build and utility scripts

## Key Files
- `src/instrument_geometry.py` - Main geometry calculations
- `src/geometry_engine.py` - Core geometric primitives
- `src/parameter_registry.py` - Parameter definitions and metadata
- `web/app.js` - Main frontend application
- `web/ui.js` - UI generation and interaction
- `web/styles.css` - All styling

## Mobile/PWA Considerations
- Test changes on mobile viewport sizes
- The app has a 56px icon bar on the left on mobile
- Modals and overlays must be outside `.app-container` for proper z-index stacking
- Cache aggressively - use `?reset` URL parameter to clear cache when testing
