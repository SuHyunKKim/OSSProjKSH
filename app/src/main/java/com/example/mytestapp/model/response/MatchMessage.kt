package com.example.mytestapp.model.response

import android.os.Parcelable
import kotlinx.parcelize.Parcelize
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
// 채팅 메시지 저장 요청을 위한 데이터 모델
@Parcelize
@Serializable
data class MatchMessage(
    @SerialName("CHistoryID")
    val CHistoryID: String,
    @SerialName("senderID")
    val senderID: String,
    @SerialName("receiverID")
    val receiverID: String,
    @SerialName("content")
    val content: String
) : Parcelable
