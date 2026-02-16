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

        NumberAnimation on rotation {
            id: rotateAnim
            from: 0
            to: 360
            duration: 2000
            loops: Animation.Infinite
            running: dragArea.drag.active
        }

        MouseArea {
            id: dragArea
            anchors.fill: parent
            drag.target: centerRect
            cursorShape: Qt.OpenHandCursor

            onPressed: {
                cursorShape = Qt.ClosedHandCursor
            }

            onReleased: {
                cursorShape = Qt.OpenHandCursor
            }
        }

        Text {
            anchors.centerIn: parent
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: "drag me\n+ rotation"
        }
    }

    Row {
        id: paletteRow
        spacing: 8
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50

        function onSwatchClick(parentColor, button) {
            if (button === Qt.LeftButton) {
                centerRect.color = parentColor
            } else if (button === Qt.RightButton) {
                centerRect.color = Qt.tint(parentColor, Qt.rgba(1, 1, 1, 0.3))
            }
        }

        Repeater {
            model: [
                "#FF0000",
                "#FF7F00",
                "#FFFF00",
                "#00FF00",
                "#0000FF",
                "#4B0082",
                "#8B00FF"
            ]

            Rectangle {
                width: 15
                height: 15
                color: modelData
                border.color: "black"
                border.width: 1

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                    onClicked: paletteRow.onSwatchClick(parent.color, mouse.button)
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

