package com.example.mytestapp.model.request

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

// 채팅방 생성 요청 데이터 모델
@Serializable
data class ChatRoomRequest(
    @SerialName("userID")
    val userID: String,
    @SerialName("userID2")
    val userID2: String
)