<p align="center">
  <a href="https://aa-classic.com">
    <img src="https://aa-classic.com/_ipx/h_45&f_webp/img/logo.png" alt="AAC Logo">
  </a>
</p>

<p align="center">ArcheAge Classic Addon Repository</p>

<p align="center">
  <img src="https://img.shields.io/github/contributors-anon/classic-addon-manager/addons" alt="Contributors badge" />
</p>

This repository contains addon declarations used by Classic Addon Manager to catalogue and install addons.
As a player on ArcheAge Classic you do not need to interact with this repository in any way, the Classic Addon Manager is all you need.

### Addon descriptions
---
Classic Addon Manager will replace your addon's YAML description field when viewed in the browser if you push a file named `README.md` to the root directory of your addon's repository.

It supports most markdown elements and should faithfully recreate your README when viewed.

### How to publish your addon
---

Start by forking this repository and cloning it to your machine.

Once done add a YAML file with your addon name (see [naming conventions](#naming-conventions) below),
fill out the fields "name, description, author, repo, tags" (see [explanation of declaration](#addon-declaration-explanation) below).

Commit your changes to your forked repository and open a pull request to this repository, [you can learn more about pull requests here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

A member will review your pull request and approve it after inspecting the addon. Once accepted a new addon manifest is generated and users of the Classic Addon Manager will see your addon.

#### Addon file structure
The best way to get familiar with the addon file structure is to look at the example [located here](https://github.com/classic-addon-manager/example-plugin).
It is expected to be a flat structure with your entrypoint in the root directory of the repository.

#### Naming conventions
Ensure that your addon's YAML file matches the name as best it can, for example if the addon's name is `example-plugin`, the YAML file should be called `example-plugin.yaml`.
> [!WARNING]
> If your in-game addon uses spaces for its name then your `name` field and addon_name.yaml file MUST use underscores `_` rather than space.

#### Addon declaration explanation
A addon declaration (plugin.yaml) file must consist of 7 fields, there are also optional fields you may fill out.

1. name (required)
2. alias (required)
3. dependencies (optional)
4. description (required)
5. author (required)
6. repo (required)
7. branch (required)
8. tags (required)
9. kofi (optional)
10. keywords (optional)

`name` is the field that declares the name of the addon and is what will be put in your addons.txt file as well as your Addon directory. This field should match the filename.

`alias` is the field that allows you to declare a "friendly" name for your addon. This field is what will be displayed in the addon manager and should be representative of your addon's name.

`dependencies` is the field that allows you to declare which addons should be installed alongside with your addon if needed to operate. This allows you to publish addons as libraries for other addons to use.
If you are publishing a library please use the wording "lib" somewhere in its name to denote that it is a library and not a standalone addon.

Dependencies are a YAML array of strings representing the addon name that you depend on.
Example: 
```YAML
dependencies: ['example-plugin']
```

`description` is a short description that allows you to describe what your addon does to the user. This text is displayed in the addon manager when browsing and should ideally match the in-game description of your addon.

`author` is your name, the author. It is just used to display who made the addon and should ideally match the in-game author of your addon.

`repo` is the github username and repository combination of your addon. The example plugin's repo value is `classic-addon-manager/example-addon`. Yours is likely going to be `your-github-username/your-addon-name`.

`branch` is the github branch that is considered the main branch of your repository. By default this is 'main' unless you opted for a different name while creating your repository.

`tags` is a string array determining ways to indicate what your addon is about to the end user as well as being possible to filter on. Ensure you surround your tags with single quotes `'`

`kofi` is your username on [ko-fi.com](https://ko-fi.com), ko-fi is a service that allows users to support you monetarily as a creator. If you add a ko-fi username your addon will show a "support author" section.

`keywords` is the field used by the Daru AI Assistant to help recommend your addons to users. It is the best and most important way to have your addon discovered through the use of the Daru Assistant.

Each keyword must be one word, no spaces allowed. If you want to use dashes you **must** quote it using quotes! It is recommended to use simple keywords that describe your addon. 

There's a total limit of 255 characters combined (each word + 1 space). This should allow up to ~25-50 depending keywords depending on the length.

Here's how you use it:

```yaml
keywords:
  - crafting
  - naval
  - pve
```

#### Generate an addon YAML file from a form
You can easily generate a YAML file by going to the following URL and entering the data as needed. It's important to still understand what each field does but this tool is designed to assist you in creating the file.

![Create your YAML file here.](https://aac.gaijin.dev/addon/create)

### How to push updates to users
Classic Addon Manager uses github releases to push updates to users.
When you are ready to push and update simply go to github and create a release, once done users will be notified of your update in the addon manager.

[You can learn more about github releases here](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

In simple steps:

1. Create a tag for the version you are happy with. We suggest using `1.0.0` for your first version. You can do this with two commands: `git tag 1.0.0` to create the tag and `git push --tags` to push the tag to github.
2. Go to your github addon repository and click the link `Create a new release`.
3. Fill out your release information and press `Publish release`
4. Sit back and relax as the addon manager propagates the changes to the players.


