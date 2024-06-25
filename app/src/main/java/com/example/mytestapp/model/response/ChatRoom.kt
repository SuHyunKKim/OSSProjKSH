package com.example.mytestapp.model.response

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
// 채팅 메시지 저장 요청을 위한 데이터 모델
@Serializable
data class ChatRoom(
    @SerialName("HistoryID")
    val HistoryID: String,
    @SerialName("userID")
    val userID: String,
    @SerialName("userID2")
    val userID2: String
)

