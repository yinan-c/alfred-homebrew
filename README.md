# Easy Homebrew
It is an Alfred workflow for you to easy brew on Alfred -- Search, get details and run Homebrew commands.

## Requirments
- Required: Python3, [Alfred PowerPack](https://www.alfredapp.com/powerpack/)
- [Homebrew](https://brew.sh/) required to view and run commands, searching for casks and formulae information does not rely on homebrew.

## Usage

- Simply type `brew` to show and search for all formulae and casks
  - by default, casks will be listed first, you can add 'cask' or 'formula' to your query (before or after) to further filter results (for example `brew vim formula` or `brew formula vim` will filter out casks results and only list formula.
  - Quicklook information page on brew.sh by pressing `command + Y` on selected entries.

![](https://i.imgur.com/ucsFm1l.png)

- Continue to **type the full name** or **tab-complete** the selected items (if enabled in Alfred) to show details of information (Analytics, install status and newest versions, urls ...) and commands, commands include install, uninstall, upgrade, show info ... Commands will depend on install status. 
- Alternatively, in the dropdown list, select any items and press `enter` to see more details and applicable commands.

   - Press `enter` on urls will open them in the browser, on commands will run them in terminal.
   - Quicklook urls are supported for all urls.

![](https://i.imgur.com/NjZ3EgR.png)

- View lists of homebrew leaves, installed formulae and casks, and outdated ones by typing keywords `leaves`, `list` and `outdated`.
  - I also added the default search_keyword `brew` to show installed and outdated lists, so that you can see whether a package is installed, or outdated. 
  - In the outdated list, you can update one-by-one or all-at-once with a simple `enter`.
  - In `leaves` and `list`, tab-complete to view info and `enter` to view/run commands as you do with default `brew` search.
  - In `leaves`, quicklook is also available.

![](https://i.imgur.com/67Is56w.png)
![](https://i.imgur.com/tMsw96l.png)
![](https://i.imgur.com/DdPJLLu.png)

**PS:** In the scripts, every function returns results based on `brewtype` (either `cask` or `formula`), you can modify keywords and function arguments to make this workflow to the best your needs.

## Thanks
- Icon from [Bukeicon](https://www.flaticon.com/authors/bukeicon), [Freepik](https://www.flaticon.com/authors/freepik) on [flaticon.com](https://www.flaticon.com)
- [Alfred forum](https://www.alfredforum.com/topic/20515-homebrew-workflow-learn-more-about-formulas-and-casks/)
