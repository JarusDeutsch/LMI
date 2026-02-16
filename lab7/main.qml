import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    width: 400
    height: 450

    Rectangle {
        anchors.fill: parent
        color: "white"
    }

    property real vGap: 40

    property real squareSize: Math.min(width, height - 120 - vGap) / 2

    Rectangle {
        id: topLeft
        width: root.squareSize
        height: root.squareSize
        color: "#880000"
        x: 0
        y: 0

        Text {
            text: 'color: "#880000"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: topRight
        width: root.squareSize
        height: root.squareSize
        color: "#FF0000"
        x: root.width - root.squareSize
        y: 0

        Text {
            text: 'color: "#FF0000"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: bottomLeft
        width: root.squareSize
        height: root.squareSize
        color: "#00FF00"
        x: 0
        y: root.squareSize + root.vGap

        Text {
            text: 'color: "#00FF00"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: bottomRight
        width: root.squareSize
        height: root.squareSize
        color: "#008800"
        x: root.width - root.squareSize
        y: root.squareSize + root.vGap

        Text {
            text: 'color: "#008800"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: centerRect
        width: root.squareSize * 1.2
        height: root.squareSize * 1.2
        color: "royalblue"
        radius: 25
        antialiasing: true
        x: (root.width - width) / 2
        y: root.squareSize + root.vGap / 2 - height / 2
        transformOrigin: Item.Center
        rotation: -45

        Text {
            anchors.centerIn: parent
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: 'color: "royalblue"\nradius: 25\nrotation: -45'
        }
    }

    Row {
        id: paletteRow
        spacing: 8
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50

        function makeSwatch(colorString) {
            return Qt.createQmlObject('import QtQuick 2.15; Rectangle { ' +
                                      'width: 15; height: 15; color: "' + colorString + '"; ' +
                                      'border.color: "black"; border.width: 1 }',
                                      paletteRow, "swatch_" + colorString)
        }

        Rectangle {
            width: 15
            height: 15
            color: "#FF0000"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#FF7F00"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#FFFF00"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#00FF00"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#0000FF"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#4B0082"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.tint(parent.color, Qt.rgba(1, 1, 1, 0.3))
                    }
                }
            }
        }

        Rectangle {
            width: 15
            height: 15
            color: "#8B00FF"
            border.color: "black"
            border.width: 1

            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if (mouse.button === Qt.LeftButton) {
                        centerRect.color = parent.color
                    } else if (mouse.button === Qt.RightButton) {
                        centerRect.color = Qt.lighter(parent.color, 130)
                    }
                }
            }
        }
    }

    Button {
        id: exitButton
        text: qsTr("Вихід")
        anchors.top: paletteRow.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 10
        onClicked: Qt.quit()
    }
}

