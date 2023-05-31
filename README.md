# Easy Homebrew
An Alfred workflow to make homebrew right on Alfred -- search, get details and run commands.

## Requirments
- Required: Python3, [Alfred PowerPack](https://www.alfredapp.com/powerpack/)
- [Homebrew](https://brew.sh/) required to view and run commands, searching for casks and formulae information does not rely on homebrew.

## Usage

- Simply type `brew` to show and search for all formulae and casks
  - by default, casks will be listed first, you can add 'cask' or 'formula' to your query (before or after) to further filter results (for example `brew vim formula` or `brew formula vim` will filter out casks results and only list formula.
  - Quicklook information page on brew.sh by press `command + Y` on selected entries.

![](https://i.imgur.com/ucsFm1l.png)

- Continue to **type full name** or **tab-complete** the selected items (if enabled in Alfred) to show details of information (Analytics, install versions and newsest versions, urls ...).
   - Press `enter` on urls will open them in browser.
   - Quicklook urls are supported for all urls.

![](https://i.imgur.com/DqVLWzu.png)


- In the dropdown list, select any items and press `enter` to see more details and applicable commands, commands include install, uninstall, upgrade, show info ... Commands will depends on install status.

![](https://i.imgur.com/30rtVus.png)

- View lists of homebrew leaves, installed formulae and casks, and outdated ones by type keywords `leaves`, `list` and `outdated`.
  - I also added default search_keyword `brew` to show installed and outdated lists, so that you can see whether a package is installed, or outdated. 
  - In outdated list, you can update one-by-one or all-at-once with a simple `enter`.
  - In `leaves` and `list`, tab-complete to view info and `enter` to view/run commands are also available.
  - In `leaves`, quicklook is also avaibles.

![](https://i.imgur.com/tMsw96l.png)
![](https://i.imgur.com/NaYjGaw.png)


**PS:** In the scripts, every function returns results based on `brewtype` (either `cask` or `formula`), you can modify you own keywords and function arguments to make this workflow to the best your needs.

## Thanks
- Icon from [Bukeicon](https://www.flaticon.com/authors/bukeicon), [Freepik](https://www.flaticon.com/authors/freepik) on [flaticon.com](https://www.flaticon.com)
- [Alfred forum](https://www.alfredforum.com/topic/20515-homebrew-workflow-learn-more-about-formulas-and-casks/)
