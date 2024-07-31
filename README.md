# Kenyoni MKDocs Plugins

## Install

```commandline
pip install git+https://github.com/kenyoni-software/kny-mkdocs
```

## Configuration

```yml
plugins:
  - kny_badge
  - kny_common:
      # Enable admonition idea, optional
      admonition_idea: false
  - kny_godot_ref:
      # Godot documentation URL, optional
      godot_url: "https://docs.godotengine.org/en/stable"
  - kny_source_ref:
      # Source code URL, required
      source_url: "https://github.com/kenyoni-software/kny-mkdocs/tree/main"
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

### kny_godot_ref

Create a link of Godot class/type to the Godot documentation.

```
{{ kny:godot class }}
```

### kny_source_ref

Create a link relative to your source base path.

```
{{ kny:source "path/foo bar" }}
```
