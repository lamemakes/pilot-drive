<!--
Thanks for contributing to the project!
Please help us keep this project in good shape by going through this checklist.
Replace the empty checkboxes [ ] below with checked ones [X] as they are completed
Remember, you can preview this before saving it.

As with all great things, this template was adapted from Signal Desktop:
https://github.com/signalapp/Signal-Desktop/blob/main/.github/PULL_REQUEST_TEMPLATE.md
-->

### Contributor checklist:

- [ ] My commits are in nice logical chunks with [good commit messages](http://chris.beams.io/posts/git-commit/)
- [ ] My fork has been merged with the latest [PILOT Drive master branch](https://github.com/lamemakes/pilot-drive/tree/master)
- [ ] My changes pass the following code quality checks:
    - [ ] ```python3.11 -m pylint backend/pilot-drive```
    - [ ] ```python3.11 -m pytest backend/```
    <!-- Frontend linting/tests will be added soon but please confirm all looks good there too ;) -->
- [ ] A skim-through of the [documentation](https://pilot-drive.rtfd.org) has been completed and any neccesary changes have been made 
- [ ] Neccesary [pytest](https://docs.pytest.org/en/7.3.x/) (Python) and/or [vitest](https://vitest.dev/) (Vue) tests have been added <!-- Again, UI testing will be implemented soon -->

### Description

<!--
Describe briefly what your pull request changes. Focus on the value provided to users.

Does it address any outstanding issues in this project?
  https://github.com/lamemakes/pilot-drive/issues?utf8=%E2%9C%93&q=is%3Aissue
  Reference an issue with the hash symbol: "#222"
  If you're fixing it, use something like "Fixes #222"

Please write a summary of your test approach:
  - What kind of manual testing did you do?
  - Did you write any new tests?
  - What Linux Distros did you test with? (please use specific versions: http://whatsmyos.com/)
  - What other devices did you test with? (Android, iOS, ODB Adapters, etc.)
-->