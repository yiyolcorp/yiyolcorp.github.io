#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
# hugo -t <your theme>
hugo -t ananke

# Go to public folder, submodule commit
cd public
# Add changes to git.
echo "*** =============="
git add .
echo "=============="

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"
echo "=============="

# Push source and build repos.
echo "+++ =============="
git push origin gh-pages
echo "--- =============="

# Come back up to the project root
cd ..

# Commit and push to master branch
git add .

echo "=============="

msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push origin master

