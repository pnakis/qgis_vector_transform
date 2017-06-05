# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorTranformation
                                 A QGIS plugin
 This plugin applies transformations on vector layers.
                             -------------------
        begin                : 2017-06-04
        copyright            : (C) 2017 by Panagiotis Nakis
        email                : pnakis@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load VectorTranformation class from file VectorTranformation.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .vector_transform import VectorTranformation
    return VectorTranformation(iface)
