gulp = require 'gulp'
changed = require 'gulp-changed'
coffee = require 'gulp-coffee'
coffeelint = require 'gulp-coffeelint'
htmlhint = require 'gulp-htmlhint'
csslint = require 'gulp-csslint'
bower = require 'gulp-bower-files'
rimraf = require 'gulp-rimraf'


#
# Clean
#
gulp.task 'clean', () ->
    gulp.src 'build',
        read: false
    .pipe rimraf()


#
# Coffeescript
#
gulp.task 'build.coffee', () ->
    gulp.src 'src/**/*.coffee'
    .pipe changed 'build',
        extension: '.js'
    .pipe coffeelint()
    .pipe coffeelint.reporter()
    .pipe coffee()
    .pipe gulp.dest 'build'


#
# HTML
#
gulp.task 'build.html', () ->
    gulp.src 'src/**/*.html'
    .pipe changed 'build'
    .pipe htmlhint()
    .pipe htmlhint.reporter()
    .pipe gulp.dest 'build'


#
# CSS
#
gulp.task 'build.css', () ->
    gulp.src 'src/**/*.css'
    .pipe changed 'build'
    .pipe csslint()
    .pipe csslint.reporter()
    .pipe gulp.dest 'build'


#
# Libraries
#
gulp.task 'build.libs', () ->
    bower()
    .pipe gulp.dest 'build/libs'


#
# Others 
#
gulp.task 'build', ['clean'], () ->
    gulp.start [
        'build.coffee'
        'build.html'
        'build.css'
        'build.libs'
    ]


gulp.task 'watch', ['default'], () ->
    gulp.watch 'src/**/*.coffee', ['build.coffee']
    gulp.watch 'src/**/*.html',   ['build.html']
    gulp.watch 'src/**/*.css',    ['build.css']
    gulp.watch 'bower.json',      ['build.libs']


gulp.task 'default', [
    'build'
]

