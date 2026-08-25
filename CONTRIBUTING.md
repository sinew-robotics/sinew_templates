# Contributing to sinew_templates

Changes to visual profiles use a branch and pull request. Do not push a new style directly to `main`.

## Required workflow

1. Read `template/docs/adding-a-style.md` and the repository `AGENTS.md`.
2. Create an issue or design note that records the source, owner, license, inspection date, and academic use case.
3. Start from current `main` and create `style/<slug>`:

   ```bash
   git switch main
   git pull --ff-only
   git switch -c style/<slug>
   ```

4. Complete every item in the new-style TODO guide, including its prior-review regression catches, gallery column, plot overlay, per-style citation, documentation, zero-config demo check, and version bump.
5. Run the local quality gates listed in the guide.
6. Push the branch and open a pull request into `main`. External contributors may use the same branch name in a fork.
7. Review the downloadable gallery demo produced by CI. Attach representative screenshots to the pull request.
8. Obtain review approval and wait for every required check to pass.
9. Rebase or update the branch if `main` changed. Re-run validation after resolving conflicts.
10. Merge through the pull request, preferably with squash merge, then delete the branch.

The style pull request must not create a release tag. Releases are a separate maintainer action after the merged gallery has been reviewed on GitHub Pages.

## Recommended branch protection

Repository administrators should protect `main` with these settings:

- require a pull request before merging;
- require at least one approval;
- dismiss stale approvals after new commits;
- require the `build` job from `Build and deploy gallery`;
- require branches to be up to date;
- block force pushes and deletion;
- restrict direct pushes to maintainers only, with no routine bypass.

The workflow uploads `sinew-gallery-pr-<number>` for every pull request. It does not deploy unreviewed pull-request code over the public Pages site. Only non-PR builds deploy `main` or an approved release tag.
