#!/usr/bin/env bash

pip install .[dev]

SITE_PACKAGES=$(python -m site --user-site)
for theme in mkdocs readthedocs; do
    rm -rf $SITE_PACKAGES/mkdocs/themes/$theme
    ln -s $SITE_PACKAGES/material/templates $SITE_PACKAGES/mkdocs/themes/$theme
done
