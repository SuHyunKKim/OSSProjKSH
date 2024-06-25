package com.example.mytestapp.model.request

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
// 채팅 메시지 저장 요청을 위한 데이터 모델
@Serializable
data class ChatMessageRequest(
    @SerialName("CHistoryID")
    val CHistoryID: String,
    @SerialName("senderID")
    val senderID: String,
    @SerialName("receiverID")
    val receiverID: String,
    @SerialName("content")
    val content: String
)
