package com.example.mytestapp.viewmodel

import android.content.Context
import android.content.Intent
import android.util.Log
import android.view.MenuItem
import android.view.View
import android.widget.PopupMenu
import android.widget.Toast
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.mytestapp.R
import com.example.mytestapp.chat.ChatActivity
import com.example.mytestapp.model.request.MatchingProfile
import com.example.mytestapp.service.MatchingService
import com.example.mytestapp.entitiy.KiriServicePool
import com.example.mytestapp.model.request.ChatRoomRequest
import com.example.mytestapp.model.response.*
import com.example.mytestapp.service.ChatService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MatchingViewModel : ViewModel() {
    // LiveData 객체
    private val _matchingProfiles = MutableLiveData<List<MatchingProfile>>() // 서버로부터 받은 매칭 결과를 담는 MutableLiveData
    val matchingProfiles: LiveData<List<MatchingProfile>> = _matchingProfiles // 외부에서 관찰할 수 있는 LiveData

    private val matchingService: MatchingService = KiriServicePool.matchingService
    private val chatService: ChatService = KiriServicePool.chatService

    // 로그인 시 저장된 UserID를 SharedPreferences에서 불러와 데이터를 로드
    fun loadMatchingProfiles(context: Context) { // 서버에 매칭 결과를 요청하는 로직
        val sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        val userId = sharedPreferences.getString("UserID", null)

        // 서버로부터 받은 매칭 결과를 LiveData를 통해 MatchingFragment에 전달
        userId?.let {
            matchingService.getMatchingProfiles(it).enqueue(object : Callback<List<MatchingProfile>> {
                override fun onResponse(call: Call<List<MatchingProfile>>, response: Response<List<MatchingProfile>>) {
                    if (response.isSuccessful) {
                        val profiles = response.body()
                        // 매칭 프로필을 5명의 사용자 프로필로 변환하여 MutableLiveData에 설정
                        val userProfiles = mutableListOf<MatchingProfile>()
                        profiles?.forEach { profile ->
                            userProfiles.add(MatchingProfile(profile.matchId, profile.userId, profile.user1ID, profile.user1Name, profile.user1StudentId))
                            userProfiles.add(MatchingProfile(profile.matchId, profile.userId, profile.user2ID, profile.user2Name, profile.user2StudentId))
                            userProfiles.add(MatchingProfile(profile.matchId, profile.userId, profile.user3ID, profile.user3Name, profile.user3StudentId))
                            userProfiles.add(MatchingProfile(profile.matchId, profile.userId, profile.user4ID, profile.user4Name, profile.user4StudentId))
                            userProfiles.add(MatchingProfile(profile.matchId, profile.userId, profile.user5ID, profile.user5Name, profile.user5StudentId))
                        }
                        _matchingProfiles.value = userProfiles
                    } else {
                        Toast.makeText(context, "매칭 결과를 불러오는데 실패했습니다.", Toast.LENGTH_SHORT).show()
                        _matchingProfiles.value = emptyList()
                    }
                }

                override fun onFailure(call: Call<List<MatchingProfile>>, t: Throwable) {
                    Log.e("MatchingViewModel", "Failed to load matching profiles", t)
                    Toast.makeText(context, "매칭 결과를 불러오는데 실패했습니다.", Toast.LENGTH_SHORT).show()
                    _matchingProfiles.value = emptyList()
                }
            })
        }
    }

    // 프로필을 클릭했을 때 ChatActivity로 이동하는 로직
    fun onProfileClicked(view: View, profile: MatchingProfile) {
        val context = view.context

        // 특정 사용자 ID 및 이름 설정
        val userID2 = profile.user1ID
        val targetUserName = profile.user1Name

        // SharedPreferences에서 현재 사용자 ID 가져오기
        val sharedPreferences = context.getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        val currentUserId = sharedPreferences.getString("UserID", null) ?: return

        // 채팅방 존재 여부 확인을 위한 요청 객체 생성
        val chatRoomRequest = ChatRoomRequest(
            userID = currentUserId,
            userID2 = userID2,
        )

        // 채팅방 생성 또는 존재 여부 확인 요청
        chatService.createChatRoom(chatRoomRequest).enqueue(object : Callback<ChatRoomResponse> {
            override fun onResponse(call: Call<ChatRoomResponse>, response: Response<ChatRoomResponse>) {
                if (response.isSuccessful) {
                    val chatRoom = response.body()?.chatRoom
                    fetchChatHistory(view, currentUserId, userID2, targetUserName, chatRoom!!)
//                    if (chatRoom != null) {
//                        // 채팅방 생성에 성공한 경우 바로 채팅 액티비티로 이동
//                        moveToChatActivity(view, chatRoom, null, targetUserName)
//                    } else {
//                        Toast.makeText(context, "채팅방을 생성하지 못했습니다.", Toast.LENGTH_SHORT).show()
//                    }
                } else {
                      Toast.makeText(context, "채팅방을 생성하지 못했습니다.", Toast.LENGTH_SHORT).show()
                    // 채팅방이 이미 존재하는 경우 채팅 내역 불러오기
//                    val chatRoom = response.body()?.chatRoom
//                    fetchChatHistory(view, currentUserId, userID2, targetUserName, chatRoom!!)
                }
            }

            override fun onFailure(call: Call<ChatRoomResponse>, t: Throwable) {
                Log.e("MatchingViewModel", "Failed to create chat room", t)
                Toast.makeText(context, "네트워크 오류", Toast.LENGTH_SHORT).show()
            }
        })
    }

    // 채팅 내역 가져오기
    fun fetchChatHistory(view: View, currentUserId: String, userID2: String, targetUserName: String,
                            chatRoom: ChatRoom) {
        val context = view.context
        val userID = currentUserId
        val userID2 = userID2
//        val chatHistoryRequest = mapOf("userID" to currentUserId, "userID2" to userID2)

        chatService.getChatHistory(userID, userID2).enqueue(object : Callback<ChatRoomFetchResponse> {
            override fun onResponse(call: Call<ChatRoomFetchResponse>, response: Response<ChatRoomFetchResponse>) {
                if (response.isSuccessful) {
                    val chatHistory = response.body()?.chatMessages
                    val chatroom = ChatRoom(
                        HistoryID = chatRoom.HistoryID, // 여기서 채팅방의 실제 HistoryID를 가져와야 합니다
                        userID = currentUserId,
                        userID2 = userID2
                    )
                    moveToChatActivity(view, chatroom, chatHistory, targetUserName)
                } else {
                    Toast.makeText(context, "채팅 내역 요청 실패", Toast.LENGTH_SHORT).show()
                }
            }

            override fun onFailure(call: Call<ChatRoomFetchResponse>, t: Throwable) {
                Log.e("MatchingViewModel", "Failed to fetch chat history", t)
                Toast.makeText(context, "네트워크 오류", Toast.LENGTH_SHORT).show()
            }
        })
    }

    // ChatActivity로 이동
    private fun moveToChatActivity(view: View, chatRoom: ChatRoom, chatHistory: List<ChatMessage>?, targetUserName: String) {
        val context = view.context
        val intent = Intent(context, ChatActivity::class.java).apply {
            putExtra("chatRoomId", chatRoom.HistoryID)
            putExtra("targetUserId", chatRoom.userID2)
            putExtra("targetUserName", targetUserName)
            putParcelableArrayListExtra("chatHistory", chatHistory?.let { ArrayList(it) })
        }
        context.startActivity(intent)
    }

    // 메뉴 버튼을 클릭했을 때의 로직
    fun onMenuButtonClicked(view: View) {
        val popupMenu = PopupMenu(view.context, view)
        popupMenu.inflate(R.menu.item_menu)
        popupMenu.setOnMenuItemClickListener { item: MenuItem ->
            when (item.itemId) {
                R.id.nav_home -> {
                    // 홈으로 이동하는 로직
                    true
                }
                R.id.nav_roomate -> {
                    // 룸메이트 추천으로 이동하는 로직
                    true
                }
                R.id.nav_chat -> {
                    // 채팅으로 이동하는 로직
                    true
                }
                R.id.nav_mypage -> {
                    // 마이페이지로 이동하는 로직
                    true
                }
                else -> false
            }
        }
        popupMenu.show()
    }
}
