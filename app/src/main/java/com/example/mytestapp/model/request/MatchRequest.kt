package com.example.mytestapp.model.request

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class MatchRequest(
    @SerialName("userId")
    val userId: String,
    @SerialName("userId2")
    val userId2: String
)