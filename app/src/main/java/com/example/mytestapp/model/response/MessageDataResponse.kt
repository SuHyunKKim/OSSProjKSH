package com.example.mytestapp.model.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MessageDataResponse(
    @SerialName("success")
    val success: Boolean,
    @SerialName("chatroom")
    val chatroom: ChatRoom, // 채팅방 정보
    @SerialName("chat_history")
    val chat_history: List<ChatMessage> // 채팅 내역
)

