package com.example.mytestapp.model.response

import android.os.Parcelable
import kotlinx.parcelize.Parcelize
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Parcelize
@Serializable
data class ChatMessage(
    @SerialName("CHistoryID")
    val CHistoryID: String,
    @SerialName("senderID")
    val senderID: String,
    @SerialName("receiverID")
    val receiverID: String,
    @SerialName("content")
    val content: String,
    @SerialName("isMatchRequest")
    val isMatchRequest: Boolean = false // 매칭 요청 메시지 여부를 나타내는 필드 추가
) : Parcelable
