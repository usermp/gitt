# gitt - A CLI for Better Commit Messages

`gitt` is a command-line interface (CLI) tool that helps you write better commit messages by providing a structured way to select commit types and enter commit messages.

## Features

- Select commit types from a predefined list.
- Choose specific files to add to the commit or add all changes.
- Format commit messages automatically based on the selected type.

## Prerequisites

Before installing `gitt`, ensure you have the following dependencies installed:

- [Git](https://git-scm.com/)
- [fzf](https://github.com/junegunn/fzf)

## Installation

To install `gitt`, follow these steps:

1. Clone the repository.
2. Run the installation script:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   This will install `gitt` to `/usr/local/bin/`.

## Usage

To use `gitt`, simply run the following command in your terminal:

```bash
gitt
```

Follow the prompts to select files, choose a commit type, and enter your commit message.

## Commit Types

| Commit Type | Description                                                        |
|-------------|--------------------------------------------------------------------|
| no type     | No specific type selected; use when the change is minor or unclear.|
| feat        | A new feature                                                      |
| fix         | A bug fix                                                          |
| chore       | Routine tasks and maintenance                                      |
| refactor    | Code changes that do not affect functionality                      |
| docs        | Documentation changes                                              |
| style       | Formatting changes (no code change)                                |
| test        | Adding or updating tests                                           |
| perf        | Performance improvements                                           |
| ci          | Changes related to continuous integration                          |
| build       | Changes related to the build process                               |
| revert      | Reverting previous changes                                         |

This table clearly explains each commit type and its purpose.

## Acknowledgments

This project was inspired by the work of [Sina Bayandorian](https://github.com/sina-byn/gitt), whose project `gitt` provided valuable insights into creating a CLI for better commit messages.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.