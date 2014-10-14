###
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['fermata', 'utils'], \
       (fermata, utils) ->
  return fermata
      .json()
      .api
      .v1
