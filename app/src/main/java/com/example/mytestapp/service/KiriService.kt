package com.example.mytestapp.service

import com.example.mytestapp.model.request.*
import com.example.mytestapp.model.response.*
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query
import retrofit2.http.Path


// Retrofit 인터페이스 정의
interface SignService {
    @POST("signup/")
    fun signup(@Body request: signuprequest): Call<signupresponse>

    @POST("login/")
    fun login(@Body request: loginrequest): Call<loginresponse>
}

interface ProfileService {
    @POST("profilecreate/")
    fun profile(@Body request: profilerequest): Call<profileresponse>
}

interface RoommateService {
    @POST("userprefcreate/")
    fun roommate(@Body request: roommaterequest): Call<roommateresponse>
}

interface ChatService {

    @POST("chatroomcreate/")
    fun createChatRoom(@Body request: ChatRoomRequest): Call<ChatRoomResponse>

    @GET("getchathistory/")
    fun getChatHistory(@Query("userID") userID: String,
                       @Query("userID2") userID2: String): Call<ChatRoomFetchResponse>

    @GET("chatroomlist/")
    fun getChatRoomList(@Query("userID") userID: String): Call<List<ChatRoom>>

    @POST("savemessage/")
    fun saveMessage(@Body request: ChatMessageRequest): Call<ResponseBody>



    @POST("blockuser/")
    fun blockUser(@Body blockData: BlockData): Call<BlockResponse>

}

interface ReportService {
    @POST("reportuser/")
    fun reportUser(@Body reportData: ReportData): Call<ReportResponse>
}

// 사용자 정보를 조회
interface UserService {

    @GET("api/user/{user_id}/")
    fun getUserInfo(@Path("user_id") userId: String): Call<UserResponse>

}

// 매칭 관련 api
interface MatchingService {
    @GET("getmatchresult/")
    fun getMatchingProfiles(@Query("userId") userId: String): Call<List<MatchingProfile>>

    // 매칭 요청
    @POST("matchrequest/")
    fun requestMatch(@Body matchRequest: MatchRequest): Call<MatchResponse>

    // 매칭 수락
    @POST("matchaccept/")
    fun acceptMatch(@Body matchRequest: MatchRequest): Call<MatchResponse>

    // 매칭 거절
    @POST("matchreject/")
    fun rejectMatch(@Body matchRequest: MatchRequest): Call<MatchResponse>
}


interface AlgorithmService {
    @POST("matching/")
    fun algoOPS(@Body request: Algorequest): Call<Algoresponse>
}