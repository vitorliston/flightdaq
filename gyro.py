#!/usr/bin/python
# -*- coding: utf-8 -*-

# GAUL 2017 - Phil

import os, sys


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt3DCore import *
from PyQt5.Qt3DExtras import *
from PyQt5.Qt3DInput import *
from PyQt5.Qt3DRender import *
from PyQt5 import QtWidgets



class RocketView3D(Qt3DWindow):
    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y() / -20.0
        lens = self.camera().lens()
        fov = lens.fieldOfView()
        newFov = min(max(fov + delta, 20.0), 120.0)
        lens.setFieldOfView(newFov)


class GyroApp(QWidget):



    def __init__(self,layout, parent=None):


        view3D = self.view3D = RocketView3D()
        view3D.renderSettings().setRenderPolicy(QRenderSettings.OnDemand)
        viewContainer = self.viewContainer = QWidget.createWindowContainer(view3D)



        layout.addWidget(viewContainer)
        self.viewScene, self.rocketTransform = createScene()

        # Camera
        viewCam = self.viewCam = view3D.camera()
        viewCam.lens().setPerspectiveProjection(50.0, 16.0 / 9.0, 0.1, 1000.0)
        viewCam.setPosition(QVector3D(30.0, 30.0, -30.0))
        viewCam.setViewCenter(QVector3D(0.0, 0.0, 0.0))

        # Camera controls
        camCtrl = self.viewCamCtrl = QOrbitCameraController(self.viewScene)
        camCtrl.setLinearSpeed(0)
        camCtrl.setLookSpeed(-200.0)
        camCtrl.setCamera(self.viewCam)

        view3D.setRootEntity(self.viewScene)

        view3D.show()
        self.i = 0


    def updateTickInfo(self):
        self.i += 1
        self.rocketTransform.setRotation(QQuaternion.fromEulerAngles(self.i, 0, 0))


def createScene():
    rootEntity = QEntity()

    rocketEntity = QEntity(rootEntity)
    rocketMesh = QMesh()
    rocketMesh.setSource(QUrl.fromLocalFile('m4.obj'))

    rocketTransform = QTransform()

    rocketMaterial = QDiffuseMapMaterial(rootEntity)
    rocketTexture = QTextureImage()
    rocketTexture.setSource(QUrl.fromLocalFile('m4.png'))
    rocketMaterial.diffuse().addTextureImage(rocketTexture)
    rocketMaterial.setShininess(2.0)
    rocketMaterial.setAmbient(QColor.fromRgbF(0.5, 0.5, 0.5, 1.0))

    rocketEntity.addComponent(rocketMesh)
    rocketEntity.addComponent(rocketTransform)
    rocketEntity.addComponent(rocketMaterial)
    rocketTransform.setRotation(QQuaternion.fromEulerAngles(0, 0, 0))
    xBarEntity = QEntity(rootEntity)
    xBarMesh = QCylinderMesh()
    xBarMesh.setLength(50)
    xBarMesh.setRadius(0.1)
    xBarMesh.setSlices(4)
    xBarTransform = QTransform()
    xBarTransform.setRotation(QQuaternion.fromEulerAngles(0, 0, 90))
    xBarTransform.setTranslation(QVector3D(xBarMesh.length() / 2, 0, 0))
    xBarMaterial = QPhongMaterial(rootEntity)
    xBarMaterial.setAmbient(Qt.red)
    xBarMaterial.setDiffuse(Qt.red)
    xBarMaterial.setShininess(0)
    xBarEntity.addComponent(xBarMesh)
    xBarEntity.addComponent(xBarTransform)
    xBarEntity.addComponent(xBarMaterial)

    yBarEntity = QEntity(rootEntity)
    yBarMesh = QCylinderMesh()
    yBarMesh.setLength(50)
    yBarMesh.setRadius(0.1)
    yBarMesh.setSlices(4)
    yBarTransform = QTransform()
    yBarTransform.setRotation(QQuaternion.fromEulerAngles(90, 0, 0))
    yBarTransform.setTranslation(QVector3D(0, 0, -yBarMesh.length() / 2))
    yBarMaterial = QPhongMaterial(rootEntity)
    yBarMaterial.setAmbient(Qt.green)
    yBarMaterial.setDiffuse(Qt.green)
    yBarMaterial.setShininess(0)
    yBarEntity.addComponent(yBarMesh)
    yBarEntity.addComponent(yBarTransform)
    yBarEntity.addComponent(yBarMaterial)

    zBarEntity = QEntity(rootEntity)
    zBarMesh = QCylinderMesh()
    zBarMesh.setLength(50)
    zBarMesh.setRadius(0.1)
    zBarMesh.setSlices(4)
    zBarTransform = QTransform()
    zBarTransform.setTranslation(QVector3D(0, zBarMesh.length() / 2, 0))
    zBarMaterial = QPhongMaterial(rootEntity)
    zBarMaterial.setAmbient(Qt.blue)
    zBarMaterial.setDiffuse(Qt.blue)
    zBarMaterial.setShininess(0)
    zBarEntity.addComponent(zBarMesh)
    zBarEntity.addComponent(zBarTransform)
    zBarEntity.addComponent(zBarMaterial)

    return rootEntity, rocketTransform


