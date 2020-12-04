$ErrorActionPreference = 'Stop'

$current_location = $PWD.Path
cd $PSScriptRoot

try {
    gi dist -ErrorAction SilentlyContinue | rm -Force -recurse
    # & pipenv install
    & pipenv run pyinstaller -F -i config/bookscraper.ico -n BookScraper main.py
    cp params.yml dist
    cp config dist -recurse
    rm dist/config/*.ico
    write "BUILD SUCCESSFUL"
}
catch {
    write "BUILD FAILED"
    throw $_
}
finally {
    cd $current_location
}
