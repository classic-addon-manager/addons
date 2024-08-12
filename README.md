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

### How to publish your addon

Start by forking this repository and cloning it to your machine.

Once done add a YAML file with your plugin name (see [naming conventions](#naming-conventions) below),
fill out the fields "name, description, author, repo, tags" (see [explanation of declaration](#addon-declaration-explanation) below).

Commit your changes to your forked repository and open a pull request to this repository, [you can learn more about pull requests here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

A member will review your pull request and approve it after inspecting the addon. Once accepted a new addon manifest is generated and users of the Classic Addon Manager will see your addon.

##### Addon file structure
The best way to get familiar with the addon file structure is to look at the example [located here](https://github.com/classic-addon-manager/example-plugin).
It is expected to be a flat structure with your entrypoint in the root directory of the repository.

##### Naming conventions
Ensure that your addon's YAML file matches the name as best it can, for example if the addon's name is `example-plugin`, the YAML file should be called `example-plugin.yaml`.

##### Addon declaration explanation
A addon declaration (plugin.yaml) file consists of 5 fields.

1. name
2. description
3. author
4. repo
5. tags

`name` is the field that declares the name of the addon and is what will be put in your addons.txt file as well as your Addon directory. This field should ideally match the filename.

`description` is a short description that allows you to describe what your addon does to the user. This text is displayed in the addon manager when browsing and should ideally match the in-game description of your addon.

`author` is your name, the author. It is just used to display who made the addon and should ideally match the in-game author of your addon.

`repo` is the github username and repository combination of your addon. The example plugin's repo value is `classic-addon-manager/example-addon`. Yours is likely going to be `your-github-username/your-addon-name`.

`tags` is a string array determining ways to indicate what your addon is about to the end user as well as being possible to filter on. Ensure you surround your tags with single quotes `'`

### How to push updates to users
Classic Addon Manager uses github releases to push updates to users.
When you are ready to push and update simply go to github and create a release, once done users will be notified of your update in the addon manager.

[You can learn more about github releases here](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
