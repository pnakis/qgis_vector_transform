# -*- coding: utf-8 -*-
"""
/***************************************************************************
 VectorTranformation
                                 A QGIS plugin
 This plugin applies transformations on vector layers.
                              -------------------
        begin                : 2017-06-04
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Panagiotis Nakis
        email                : pnakis@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QDialogButtonBox
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from vector_transform_dialog import VectorTranformationDialog
import os.path
from qgis.core import *
import math


class VectorTranformation:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'VectorTranformation_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Vector Transformation')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'VectorTranformation')
        self.toolbar.setObjectName(u'VectorTranformation')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('VectorTranformation', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = VectorTranformationDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/VectorTranformation/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Transform'),
            callback=self.run,
            parent=self.iface.mainWindow())
        # ALL CONNECT SIGNALS
        # pushButton_Save dialog
        self.dlg.pushButton_Save.clicked.connect(self.select_output_location)
        # See if Transformation List has changed and send singal to function
        self.dlg.comboBoxTransf.currentIndexChanged.connect(self.selectionchange)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Vector Transformation'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        
        
    # Detect the selected transformation from the list and enable / disable input fields
    def selectionchange(self,i):
        # Transformation selection function
        if i == 1: #Translation
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(True);self.dlg.doubleSpinBox_y_t.setEnabled(True)
            self.dlg.doubleSpinBox_x_r.setEnabled(False);self.dlg.doubleSpinBox_y_r.setEnabled(False)
            self.dlg.doubleSpinBox_x_s.setEnabled(False);self.dlg.doubleSpinBox_y_s.setEnabled(False)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True);
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("X Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("X Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'Translation'

        elif i == 2: #Rotaion
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(False);self.dlg.doubleSpinBox_y_t.setEnabled(False)
            self.dlg.doubleSpinBox_x_r.setEnabled(True);self.dlg.doubleSpinBox_y_r.setEnabled(True)
            self.dlg.doubleSpinBox_x_s.setEnabled(False);self.dlg.doubleSpinBox_y_s.setEnabled(False)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True)
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("X Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("X Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'Rotation'

        elif i == 3: #Scale
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(False);self.dlg.doubleSpinBox_y_t.setEnabled(False)
            self.dlg.doubleSpinBox_x_r.setEnabled(False);self.dlg.doubleSpinBox_y_r.setEnabled(False)
            self.dlg.doubleSpinBox_x_s.setEnabled(True);self.dlg.doubleSpinBox_y_s.setEnabled(True)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True)
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("X Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("X Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'Scale'

        elif i == 4: #Similarity
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(True);self.dlg.doubleSpinBox_y_t.setEnabled(True)
            self.dlg.doubleSpinBox_x_r.setEnabled(True);self.dlg.doubleSpinBox_y_r.setEnabled(False)
            self.dlg.doubleSpinBox_x_s.setEnabled(True);self.dlg.doubleSpinBox_y_s.setEnabled(False)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True)
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'Similarity'

        elif i == 5: #Affine
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(True);self.dlg.doubleSpinBox_y_t.setEnabled(True)
            self.dlg.doubleSpinBox_x_r.setEnabled(True);self.dlg.doubleSpinBox_y_r.setEnabled(False)
            self.dlg.doubleSpinBox_x_s.setEnabled(True);self.dlg.doubleSpinBox_y_s.setEnabled(True)
            self.dlg.doubleSpinBox_ax_th.setEnabled(True);self.dlg.doubleSpinBox_b0.setHidden(True)
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("X Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'Affine'
        elif i == 6: #Affine with coefficients
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(True);self.dlg.doubleSpinBox_y_t.setEnabled(True)
            self.dlg.doubleSpinBox_x_r.setEnabled(True);self.dlg.doubleSpinBox_y_r.setEnabled(True)
            self.dlg.doubleSpinBox_x_s.setEnabled(True);self.dlg.doubleSpinBox_y_s.setEnabled(True)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True)
            
            # Change Labels
            self.dlg.label_x_tra.setText("a1");self.dlg.label_y_tra.setText("b1")
            self.dlg.label_x_rot.setText("c1");self.dlg.label_y_rot.setText("a2")
            self.dlg.label_x_sca.setText("b2");self.dlg.label_y_sca.setText("c2")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
            global trans_meth
            trans_meth = 'AffineCoe'
        
        elif i == 7: #Projection
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.dlg.pushButton_Save.setEnabled(True);self.dlg.lineEdit.setEnabled(True)
            self.dlg.doubleSpinBox_x_t.setEnabled(True);self.dlg.doubleSpinBox_y_t.setEnabled(True)
            self.dlg.doubleSpinBox_x_r.setEnabled(True);self.dlg.doubleSpinBox_y_r.setEnabled(True)
            self.dlg.doubleSpinBox_x_s.setEnabled(True);self.dlg.doubleSpinBox_y_s.setEnabled(True)
            self.dlg.doubleSpinBox_ax_th.setEnabled(True);self.dlg.doubleSpinBox_b0.setHidden(False)
            # Change Labels
            self.dlg.label_x_tra.setText("a1");self.dlg.label_y_tra.setText("b1")
            self.dlg.label_x_rot.setText("c1");self.dlg.label_y_rot.setText("a2")
            self.dlg.label_x_sca.setText("b2");self.dlg.label_y_sca.setText("c2")
            self.dlg.label_axis_ang.setText("a0");self.dlg.label_b0.setHidden(False)
            
            global trans_meth
            trans_meth = 'Projection'
 
        else:
            # Enable/Hide Buttons
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
            self.dlg.pushButton_Save.setEnabled(False);self.dlg.lineEdit.setEnabled(False)
            self.dlg.doubleSpinBox_x_t.setEnabled(False);self.dlg.doubleSpinBox_y_t.setEnabled(False)
            self.dlg.doubleSpinBox_x_r.setEnabled(False);self.dlg.doubleSpinBox_y_r.setEnabled(False)
            self.dlg.doubleSpinBox_x_s.setEnabled(False);self.dlg.doubleSpinBox_y_s.setEnabled(False)
            self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True);self.dlg.label_b0.setHidden(True)
            # Change Labels
            self.dlg.label_x_tra.setText("X Translation");self.dlg.label_y_tra.setText("Y Translation")
            self.dlg.label_x_rot.setText("X Rotation (Degrees)");self.dlg.label_y_rot.setText("Y Rotation (Degrees)")
            self.dlg.label_x_sca.setText("X Scale");self.dlg.label_y_sca.setText("Y Scale")
            self.dlg.label_axis_ang.setText("Axis Angle (Degrees)");self.dlg.label_b0.setHidden(True)
            
    # Save button call function
    def select_output_location(self):
        
        # Save box function call
        filename = QFileDialog.getSaveFileName(self.dlg, 'Save File',"",'*.shp')
        self.dlg.lineEdit.setText(filename)
        
        self.dlg.pushButton_Save.blockSignals(False)
        
    # TRANSFORMATION FUNCTIONS
    def Translation(self,x,y):
        global xx,yy
        
        x_par = self.dlg.doubleSpinBox_x_t.value() # X Translation parameter
        y_par = self.dlg.doubleSpinBox_y_t.value() # Y Translation parameter
        
        xx = x + x_par
        yy = y + y_par

    def Rotation(self,x,y):
        global xx,yy
        
        x_par = self.dlg.doubleSpinBox_x_r.value() # X Rotation parameter
        y_par = self.dlg.doubleSpinBox_y_r.value() # Y Rotation parameter
        
        rot_x = math.radians(x_par) # Degrees to radians
        rot_y = math.radians(y_par) # Degrees to radians

        xx = math.cos(rot_x)*x + math.sin(rot_y)*y
        yy = -math.sin(rot_x)*x + math.cos(rot_y)*y
        
    def Scale(self,x,y):
        global xx,yy
        
        x_par = self.dlg.doubleSpinBox_x_s.value() # X Scale parameter
        y_par = self.dlg.doubleSpinBox_y_s.value() # Y Scale parameter
        
        xx = x*x_par
        yy = y*y_par
        
        
    def Similarity(self,x,y):
        global xx,yy
        x_par = self.dlg.doubleSpinBox_x_t.value() # X Translation parameter
        y_par = self.dlg.doubleSpinBox_y_t.value() # Y Translation parameter
        ang_par = self.dlg.doubleSpinBox_x_r.value() # Rotation parameter
        s_par = self.dlg.doubleSpinBox_x_s.value() # Scale parameter
        
        rot_xy = math.radians(ang_par) #Degrees to radians
        xx = math.cos(rot_xy)*s_par*x + math.sin(rot_xy)*s_par*y + x_par
        yy = -math.sin(rot_xy)*s_par*x + math.cos(rot_xy)*s_par*y + y_par
        
        
    def Affine(self,x,y):
        global xx,yy
        xt_par = self.dlg.doubleSpinBox_x_t.value() # X Translation parameter
        yt_par = self.dlg.doubleSpinBox_y_t.value() # Y Translation parameter
        xs_par = self.dlg.doubleSpinBox_x_s.value() # X Scale parameter
        ys_par = self.dlg.doubleSpinBox_y_s.value() # Y Scale parameter
        r_par = self.dlg.doubleSpinBox_x_r.value() # Rotation parameter
        a_par = self.dlg.doubleSpinBox_ax_th.value() # Axis Perpenticularity parameter

        rot_xy = math.radians(r_par) #Degrees to radians
        delta = math.radians(a_par) #Degrees to radians
        
        a = xs_par*(math.cos(rot_xy)+delta*math.sin(rot_xy))
        b = ys_par*math.sin(rot_xy)
        c = xs_par*(-math.sin(rot_xy)+delta*math.cos(rot_xy))
        d = ys_par*math.cos(rot_xy)
        
        xx = a*x + b*y + xt_par
        yy = c*x + d*y + yt_par
        
        
    def AffineCoe(self,x,y):
        global xx,yy
        a1 = self.dlg.doubleSpinBox_x_t.value()
        b1 = self.dlg.doubleSpinBox_y_t.value()
        c1 = self.dlg.doubleSpinBox_x_r.value()
        a2 = self.dlg.doubleSpinBox_y_r.value()
        b2 = self.dlg.doubleSpinBox_x_s.value()
        c2 = self.dlg.doubleSpinBox_y_s.value()

        xx = a1*x + b1*y + c1
        yy = a2*x + b2*y + c2
        
    def Projection(self,x,y):
        global xx,yy
        
        a1 = self.dlg.doubleSpinBox_x_t.value();b1 = self.dlg.doubleSpinBox_y_t.value()
        c1 = self.dlg.doubleSpinBox_x_r.value();a2 = self.dlg.doubleSpinBox_y_r.value()
        b2 = self.dlg.doubleSpinBox_x_s.value();c2 = self.dlg.doubleSpinBox_y_s.value()
        a0 = self.dlg.doubleSpinBox_ax_th.value();b0 = self.dlg.doubleSpinBox_b0.value()

        div = a0*x + b0*y + 1
        
        xx = (a1*x + b1*y + c1) / div
        yy = (a2*x + b2*y + c2) / div
        
        
    def run(self):
        # Set fixed plugin size
        self.dlg.setFixedSize(312, 390)
        
        #Disable buttons when the plugin starts
        self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.dlg.pushButton_Save.setEnabled(False);self.dlg.lineEdit.setEnabled(False)
        # Clear all input fields
        self.dlg.doubleSpinBox_x_t.setValue(0);self.dlg.doubleSpinBox_y_t.setValue(0)
        self.dlg.doubleSpinBox_x_r.setValue(0);self.dlg.doubleSpinBox_y_r.setValue(0)
        self.dlg.doubleSpinBox_x_s.setValue(0);self.dlg.doubleSpinBox_y_s.setValue(0)
        self.dlg.doubleSpinBox_ax_th.setValue(0);self.dlg.doubleSpinBox_b0.setValue(0)
        self.dlg.lineEdit.clear()
        self.dlg.comboBoxTransf.clear()
        # Disable all input textboxes when starting the plugin
        self.dlg.doubleSpinBox_x_t.setEnabled(False);self.dlg.doubleSpinBox_y_t.setEnabled(False)
        self.dlg.doubleSpinBox_x_r.setEnabled(False);self.dlg.doubleSpinBox_y_r.setEnabled(False)
        self.dlg.doubleSpinBox_x_s.setEnabled(False);self.dlg.doubleSpinBox_y_s.setEnabled(False)
        self.dlg.doubleSpinBox_ax_th.setEnabled(False);self.dlg.doubleSpinBox_b0.setHidden(True);self.dlg.label_b0.setHidden(True)
        # Populate Transformation List
        transf_list = ["", "Translation", "Rotation", "Scale", "Similarity", "Affine","Affine (Known coefficients)", "Projection"]
        self.dlg.comboBoxTransf.addItems(transf_list)
        
        # Clear and populate the combo box with all vector layer from the Layers Panel
        self.dlg.comboBoxLayers.clear()
        layers = self.iface.legendInterface().layers()
        # Read only vector layers and add them to the list
        layer_list = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                layer_list.append(layer.name())
        self.dlg.comboBoxLayers.addItems(layer_list)
        
        # If layer list is empty Disable Ok and Save... button, else Enable
        if not layer_list:
            self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
            self.dlg.pushButton_Save.setEnabled(False)
            self.dlg.comboBoxTransf.setEnabled(False)
        else:
            #self.dlg.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            #self.dlg.pushButton_Save.setEnabled(True)
            self.dlg.comboBoxTransf.setEnabled(True)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
        
            # Get Layer from the list by name (ignores raster layers)
            layerName = self.dlg.comboBoxLayers.currentText()
            layerSel = QgsMapLayerRegistry.instance().mapLayersByName(layerName)
            PointLayer = layerSel[0] # Input layer
            
            # Empty lists for storage
            x = []
            y = []            
            kn = []
            kl = []
            kj = []
            
            # Read fields from input layer
            fields = PointLayer.fields() 
            
            #Save location
            filename = self.dlg.lineEdit.text() 
            
            iter  = PointLayer.getFeatures()
            
            # Read layer Type
            if PointLayer.geometryType() == 0:
                # If layer type is Points and
                if PointLayer.wkbType()==QGis.WKBMultiPoint:
                    # if geometry type contains MultiPoints
                    # Start Writer 
                    writer = QgsVectorFileWriter(filename, "8859-7", fields, QGis.WKBMultiPoint, PointLayer.crs(), "ESRI Shapefile")
                    if writer.hasError() != QgsVectorFileWriter.NoError:
                        print "Error when creating shapefile: ",  writer.errorMessage()
                    for feature in iter:
                        # Fetch geometry
                        geom = feature.geometry()
                        if geom.isMultipart():
                            # Read geometry as multipoint
                            x = geom.asMultiPoint()
                            # for every point inside x 
                            for points in x:
                                # calls selected transformation function
                                func = getattr(self, trans_meth)
                                func(points[0],points[1])
                                kn.append(QgsPoint(xx,yy))
                            #write geometry and attribute
                            # add a feature
                            fet = QgsFeature()
                            fet.setGeometry(QgsGeometry.fromMultiPoint(kn))
                            fet.setAttributes(feature.attributes())
                            writer.addFeature(fet)
                            kn=[]
                        else:
                            # Read geometry as point
                            y = geom.asPoint()
                            kj = []
                            # calls selected transformation function
                            func = getattr(self, trans_meth)
                            func(y[0],y[1])
                            kj = QgsPoint(xx,yy)
                            # write geometry and attribute
                            # add a feature
                            fet = QgsFeature()
                            fet.setGeometry(QgsGeometry.fromPoint(kj))
                            fet.setAttributes(feature.attributes())
                            writer.addFeature(fet)
                else:
                    # if geometry type contains only Points
                    # Start Writer 
                    writer = QgsVectorFileWriter(filename, "8859-7", fields, QGis.WKBPoint, PointLayer.crs(), "ESRI Shapefile")
                    if writer.hasError() != QgsVectorFileWriter.NoError:
                        print "Error when creating shapefile: ",  writer.errorMessage()
                    # for every point
                    for feature in iter:
                        # Fetch geometry
                        geom = feature.geometry()
                        # Read geometry as point
                        y = geom.asPoint()
                        kj = []
                        # calls selected transformation function
                        func = getattr(self, trans_meth)
                        func(y[0],y[1])
                        kj = QgsPoint(xx,yy)
                        # write geometry and attribute
                        # add a feature
                        fet = QgsFeature()
                        fet.setGeometry(QgsGeometry.fromPoint(kj))
                        fet.setAttributes(feature.attributes())
                        writer.addFeature(fet)
                    
            elif PointLayer.geometryType() == 1:
                # If layer type is Points
                # Start Writer
                writer = QgsVectorFileWriter(filename, "8859-7", fields, QGis.WKBLineString, PointLayer.crs(), "ESRI Shapefile")
                if writer.hasError() != QgsVectorFileWriter.NoError:
                    print "Error when creating shapefile: ",  writer.errorMessage()

                for feature in iter:
                    # Fetch geometry
                    geom = feature.geometry()
                    # If feature is MultiString
                    if geom.isMultipart():
                        # Read geometry as MultiString
                        x = geom.asMultiPolyline()
                        # for every MultiLine inside the feature
                        for multiline in x:
                            # read polygon vertex and
                            for vertex in multiline:
                                # calls selected transformation function
                                func = getattr(self, trans_meth)
                                func(vertex[0],vertex[1])
                                kl.append(QgsPoint(xx,yy))
                            kn.append(kl)
                            kl =[]
                        # write geometry and attribute
                        # add a feature
                        fet = QgsFeature()
                        fet.setGeometry(QgsGeometry.fromMultiPolyline(kn))
                        fet.setAttributes(feature.attributes())
                        writer.addFeature(fet)
                        kn=[]
                    else:
                        # if geometry is String
                        y = geom.asPolyline()
                        kj = []
                        # for every vertex of the string
                        for vertex in y:
                            # calls selected transformation function
                            func = getattr(self, trans_meth)
                            func(vertex[0],vertex[1])
                            kj.append(QgsPoint(xx,yy))
                        # write geometry and attribute
                        # add a feature
                        fet = QgsFeature()
                        fet.setGeometry(QgsGeometry.fromPolyline(kj))
                        fet.setAttributes(feature.attributes())
                        writer.addFeature(fet)
                            
            elif PointLayer.geometryType() == 2:
                # If geometry is Polygon
                # Start Writer
                writer = QgsVectorFileWriter(filename, "8859-7", fields, QGis.WKBPolygon, PointLayer.crs(), "ESRI Shapefile")
                if writer.hasError() != QgsVectorFileWriter.NoError:
                    print "Error when creating shapefile: ",  writer.errorMessage()
                
                for feature in iter:
                    # Fetch geometry
                    geom = feature.geometry()
                    # If geometry is Multipolygon
                    if geom.isMultipart():
                        # Read geometry as MultiPolygon
                        x = geom.asMultiPolygon()
                        # For every polygon inside the feature
                        for poly in x:
                            for vertex in poly[0]:
                                # calls selected transformation function
                                func = getattr(self, trans_meth)
                                func(vertex[0],vertex[1])
                                kl.append(QgsPoint(xx,yy))
                            kn.append([kl])
                            kl =[]
                        # write geometry and attribute
                        # add a feature
                        fet = QgsFeature()
                        fet.setGeometry(QgsGeometry.fromMultiPolygon(kn))
                        fet.setAttributes(feature.attributes())
                        writer.addFeature(fet)
                        kn=[]
                    else:
                        # If geometry is Polygon
                        kj = []
                        # Read geometry as Polygon
                        y = geom.asPolygon()
                        for vertex in y[0]:
                            # calls selected transformation function
                            func = getattr(self, trans_meth)
                            func(vertex[0],vertex[1])
                            kj.append(QgsPoint(xx,yy))
                        # write geometry and attribute
                        # add a feature
                        fet = QgsFeature()
                        fet.setGeometry(QgsGeometry.fromPolygon([kj]))
                        fet.setAttributes(feature.attributes())
                        writer.addFeature(fet)
            else:
                # Layer is of uknown type
                print "Unknown Layer"

            # delete the writer to flush features to disk
            del writer
            
            # Display layer in the QGis Layers Panel
            disp_name = layerName + "_" + trans_meth
            disp_layer = QgsVectorLayer(filename, disp_name, "ogr")
            QgsMapLayerRegistry.instance().addMapLayer(disp_layer)