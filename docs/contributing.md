## Contributing

### Step 1. Fork this repository to your GitHub

### Step 2. Clone the repository from your GitHub

```sh
git clone https://github.com/[YOUR GITHUB ACCOUNT]/wPyProj.git
```

### Step 3. Add this repository to the remote in your local repository

```sh
git remote add upstream "https://github.com/Wanini0209/wPyProj"
```

You can pull the latest code in master branch through `git pull upstream master` afterward.

### Step 4. Check out a branch for your new feature

```sh
git checkout -b [YOUR FEATURE]
```

### Step 5. Install Prerequsite

```sh
python -m pip install pipx
python -m pipx install pipenv invoke
python -m pipx ensurepath
```

### Step 6. Create Your Own Python Virtual Environment and Install Depdencies

```sh
inv env.init-dev
```

### Step 6. Work on your new feature

### [Optional] Step 7. Install Attendees Analyzer for local test

If you want to develop it, please run:

```sh
inv build.develop
```

### Step 8. Run test cases
Make sure all test cases pass.

```sh
inv test
```

### Step 9. Run test coverage
Check the test coverage and see where you can add test cases.

```sh
inv test.cov
```

### Step 10. Reformat source code

Format your code through `black` and `isort`.

```sh
inv style.reformat
```

### Step 11. Run style check
Make sure your coding style passes all enforced linters.

```sh
inv style
```

[Optional] Check your coding style through `pylint`. Note that you do not have to fix all the issues warned by `pylint`.

```sh
inv style.pylint
```

### [Optional] Step 12. Run security check

Ensure the packages installed are secure

```sh
inv secure
```

*[Optional]* Check whether there is common security issue in the code. Note that you do not have to fix all the issues warned by `bandit`

```sh
inv secure.bandit
```
