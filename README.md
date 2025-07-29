# gitt - A CLI for Better Commit Messages with AI Support

`gitt` is a command-line interface (CLI) tool that helps you write better commit messages by providing a structured workflow, integrating AI for message generation, and offering a user-friendly interactive experience.

## Features

* Interactive file selection with `fzf`
* Choose commit types from a predefined list
* Automatically format commit messages based on selected type
* Generate commit messages using **Cloudflare AI**
* Edit AI-generated messages before finalizing
* Confirm commit before execution
* Optional GUI support (via Streamlit, coming soon)

## Prerequisites

Make sure you have the following dependencies installed:

* [Git](https://git-scm.com/)
* [fzf](https://github.com/junegunn/fzf)
* [jq](https://stedolan.github.io/jq/) – required for AI message generation
* [curl](https://curl.se/) – used to call Cloudflare AI APIs

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/gitt.git
   cd gitt
   ```

2. Install the CLI globally:

   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   This will copy the `gitt` script to `/usr/local/bin/`.

## Configuration

To enable AI commit message generation via [Cloudflare AI](https://developers.cloudflare.com/workers-ai/), you must configure your API credentials:

```bash
gitt --config-api
```

You will be prompted to enter your:

* `CLOUDFLARE_API_TOKEN`
* `CLOUDFLARE_ACCOUNT_ID`

These will be stored securely in `~/.config/gitt/.env`.

## Usage

### CLI Mode

Run the following command in a Git repository:

```bash
gitt
```

Workflow:

1. Select files to stage (or `[ALL]`).
2. Choose a commit type.
3. Choose whether to use AI to generate the commit message.
4. If AI is used:

   * AI suggests a short message.
   * You can **edit** the suggestion or accept it as-is.
5. Review the final commit message.
6. Confirm to execute the commit.

### GUI Mode (coming soon)

```bash
gitt --gui
```

## Commit Types

| Type     | Description                                             |
| -------- | ------------------------------------------------------- |
| no type  | No specific type selected; for minor or unclear changes |
| feat     | A new feature                                           |
| fix      | A bug fix                                               |
| chore    | Routine tasks and maintenance                           |
| refactor | Code refactoring without functional change              |
| docs     | Documentation updates                                   |
| style    | Code formatting changes (whitespace, etc.)              |
| test     | Adding or modifying tests                               |
| perf     | Performance improvements                                |
| ci       | Continuous integration changes                          |
| build    | Build system or dependency changes                      |
| revert   | Reverting a previous commit                             |

## Example

```bash
$ gitt
📁 Select files to stage → fzf interface opens
🔧 Select commit type → e.g., "feat"
🤖 Use AI to generate commit message? [Y/n] → Y
💡 Suggested: Add pagination to product listing
📝 You can now edit the message:
> Add pagination to product listing
✅ Final commit message: [feat] Add pagination to product listing
✔️ Commit created successfully!
```

## Acknowledgments

Inspired by [Sina Bayandorian's](https://github.com/sina-byn/gitt) original `gitt` project, with added AI integration and usability improvements.

## Contributing

Feel free to fork, improve, or suggest features via pull requests or issues.

## License

Licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
