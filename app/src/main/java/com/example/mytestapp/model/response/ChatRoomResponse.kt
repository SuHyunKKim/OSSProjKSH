package com.example.mytestapp.model.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ChatRoomResponse(
    @SerialName("success")
    val success: Boolean,
    @SerialName("chatRoom")
    val chatRoom: ChatRoom?
)
