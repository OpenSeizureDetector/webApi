# Web interface for OSD database

## Run locally

```
npm i --legacy-peer-deps
npm start
```

If you run into issues with CORS, you may need to temporarily disable web security on your browser.
If using Chromium on Ubuntu 22.04, add

```
alias chromium-dev="chromium-browser --disable-web-security --user-data-dir=$HOME/.config/chromium-dev"
```

to your ~/.bashrc file.

Then launch your browser using the command

```
chromium-dev
```
