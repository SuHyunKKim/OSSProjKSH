package com.example.mytestapp.model.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ChatRoomFetchResponse(
    @SerialName("chatMessages")
    val chatMessages: List<ChatMessage>
)
