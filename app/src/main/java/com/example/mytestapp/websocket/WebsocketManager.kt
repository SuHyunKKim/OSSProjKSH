package com.example.mytestapp.websocket

import android.util.Log
import com.example.mytestapp.model.response.ChatMessage
import okhttp3.*
import okio.ByteString
import org.json.JSONArray
import org.json.JSONObject

class WebSocketManager(
    private val chatRoomId: Int?,
    private val onMessageReceived: (List<ChatMessage>) -> Unit,
    private val onConnectionFailed: (String) -> Unit
) {
    private lateinit var webSocket: WebSocket
    private val client = OkHttpClient()
    private val serverUrl = "ws://6dcc-128-134-0-90.ngrok-free.app/ws/chat/$chatRoomId/"
    fun connect() {
        val request = Request.Builder().url(serverUrl).build()
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("WebSocket", "Connected to server")
                // 웹소켓 연결 성공 시 초기 메시지 요청
                val initMessage = JSONObject().apply {
                    put("type", "initial_load")
                    put("chatRoomId", chatRoomId)
                }
                webSocket.send(initMessage.toString())
            }
            override fun onMessage(webSocket: WebSocket, text: String) {
                handleReceivedMessage(text)
            }
            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                handleReceivedMessage(bytes.utf8())
            }
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                onConnectionFailed(t.message ?: "Unknown error")
            }
        })
    }
    private fun handleReceivedMessage(text: String) {
        try {
            val jsonObject = JSONObject(text)
            val messageType = jsonObject.optString("type")
            if (messageType == "initial_messages") {
                val messages = mutableListOf<ChatMessage>()
                val jsonArray = jsonObject.getJSONArray("messages")
                for (i in 0 until jsonArray.length()) {
                    val messageObject = jsonArray.getJSONObject(i)
                    val chatMessage = ChatMessage(
                        CHistoryID = messageObject.optString("CHistoryID", ""),
                        senderID = messageObject.optString("senderID", ""),
                        receiverID = messageObject.optString("receiverID", ""),
                        content = messageObject.optString("content", "")
                    )
                    messages.add(chatMessage)
                }
                onMessageReceived(messages)
            } else {
                val chatMessage = ChatMessage(
                    CHistoryID = jsonObject.optString("CHistoryID", ""),
                    senderID = jsonObject.optString("senderID", ""),
                    receiverID = jsonObject.optString("receiverID", ""),
                    content = jsonObject.optString("content", "")
                )
                onMessageReceived(listOf(chatMessage))
            }
        } catch (e: Exception) {
            onConnectionFailed(e.message ?: "Error parsing message")
        }
    }
    fun sendMessage(message: String) {
        webSocket.send(message)
    }
    fun disconnect() {
        webSocket.close(1000, "Closing connection")
    }
}