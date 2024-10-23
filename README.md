# Kenyoni MkDocs Plugins

## Install

```commandline
pip install git+https://github.com/kenyoni-software/kny-mkdocs@1.1.1
```

## Configuration

With their default values.

```yml
plugins:
  - kny_badge
  - kny_common:
      # Enable admonition idea
      admonition_idea: false
      # Enable MathJax
      mathjax: false
      # Enable tablesort
      tablesort: false
  - kny_external_link_icon:
      # Icon path of material mkdocs icons.
      icon: "material/open-in-new"
      # Exclude all these links starting with...
      # Empty by default.
      exclude:
        - "https://docs.godotengine.org"
  - kny_godot_ref:
      # Godot documentation URL
      godot_url: "https://docs.godotengine.org/en/stable"
  - kny_source_ref:
      source_url: ""
      # Source code URL (e.g. https://github.com/kenyoni-software/project-catta/tree/main)
```

## Plugins

### kny_badge

Create badges, with a left and right text or use shorts for special badges with icons.

```
{{ kny:badge "left text" }}
{{ kny:badge "left text" "right text" }}
{{ kny:badge "left text" --left-bg --right-bg }}

{{ kny:badge-version "version" }}
{{ kny:badge-version "version" --right-bg }}

{{ kny:badge-experimental "text" }}
{{ kny:badge-experimental "text" --right-bg }}

{{ kny:badge-download "text" }}
{{ kny:badge-download "text" --right-bg }}
```

### kny_common

#### Admonition Idea

Admonition with an idea lamp.

```
!!! idea "title"

    Text.
```

#### MathJax

Enable `pymdownx.arithmatex` settings with `generic: true` and adds MathJax javascripts.

#### Tablesort

Add the tablesort javascripts.

### kny_external_link_icon

Adds a small icon to make external links more visible.

### kny_godot_ref

Adds an option to link to a class of the Godot Documentation.

```
{{ kny:godot class_name }}
```

### kny_source_ref

Create a link relative to your source base path.

```
{{ kny:source "path/foo bar" }}
```
