This document describes the structure of the frontend application.

The application is a web frontend application which can be delivered by a
typical web-server. It is written in
[CoffeeScript 1.7](http://coffeescript.org/),
[HTML 5](http://www.w3.org/TR/html-markup/) and
[CSS 3](http://www.w3.org/Style/CSS/).


Application structure
=====================
The applications entry point is the *index.html* file. It load the
[require.js](http://requirejs.org/) library and the *index.coffee* file and
includes all required *.css* files.

The *index.coffee* file includes the require.js configuration, which maps
library names to real paths and the initial model for the whole application.

Interactive
-----------
The application uses [knockout](http://knockoutjs.com/) to bind models to the
HTML elements.

Pages
-----
A single page application pattern is used to build the pages of the application.
Each page is loaded asynchronously on the first page request from the pages
*.html* and *.coffee* files. To manage the pages,
[pages.js](http://pagerjs.com/) is used.


Folders and structure
=====================
In this folder, you can find package and dependency declarations and the build
file (see [Build](#Build)).

The whole application source is located in the *src* folder.

On the root level of the *src* folder, files like the entry point
*index.html* and *index.coffee* are located.

All the pages content and model are located in the *src/pages* folder. Each
page has a *.html* and an optional *.coffee* file. If the page needs
additional files, a folder with the same name can be used.


Build
=====
The application utilizes [npm](https://www.npmjs.org/) to declare components
required to build the application. Therefore the only build requirement is npm
itself.

The applications frontend dependencies are managed using
[bower](http://bower.io/).

The build process is driven by [gulp](http://gulpjs.com/) which collects all the
files from bower, compiles the *.coffee* files to *.js* files and stores the
build in a *build* folder.

To prepare the environment, all npm packages must be installed. This should be
done after each change on the *package.json* file. To do so, execute:

>  npm install

To install the required frontend dependencies, the following command should be
executed:

> ./node_modules/bower/bin/bower install

After executing the command above, all requirements for the build process are
installed. The next step is to build the application and populate the 'build'
folder using the following command:

>  ./node_modules/gulp/bin/gulp.js


Development
===========
During development, a watch mode can be used to rebuild all changed files and
keep the build directory populated with the latest changes. To start this watch
mode, the following command can be used:

> ./node_modules/gulp/bin/gulp.js watch

To change the frontend dependencies, the following command should be used:

> ./node_modules/bower/bin/bower --help

The build executes a lint checks for the following file types:

* *.html*
* *.css*
* *.coffee*

The linters should always be happy.


