package com.example.mytestapp.chat

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST

interface ChatService {

    @GET("messages")
    fun getMessages(): Call<List<ChatMessage>>

    @POST("messages")
    fun postMessage(@Body message: ChatMessage): Call<ChatMessage>

    @POST("block")
    fun blockUser(@Body blockData: BlockData): Call<Void>

    @POST("report")
    fun reportUser(@Body reportData: ReportData): Call<Void>
}
