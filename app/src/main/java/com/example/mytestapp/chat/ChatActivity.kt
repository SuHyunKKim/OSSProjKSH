package com.example.mytestapp.chat

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.MenuItem
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.PopupMenu
import android.widget.TextView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.drawerlayout.widget.DrawerLayout
import androidx.lifecycle.Observer
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.mytestapp.R
import com.example.mytestapp.adapters.ChatAdapter
import com.example.mytestapp.entitiy.KiriServicePool
import com.example.mytestapp.model.request.MatchRequest
import com.example.mytestapp.viewmodel.ChatRoomViewModel
import com.example.mytestapp.matchmaking.MatchmakingActivity
import com.example.mytestapp.model.response.ChatMessage
import com.example.mytestapp.model.response.MatchResponse
import com.example.mytestapp.websocket.WebSocketManager
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class ChatActivity : AppCompatActivity() {

    private lateinit var adapter: ChatAdapter
    private lateinit var messageInput: EditText
    private lateinit var recyclerView: RecyclerView
    private lateinit var sendButton: Button
    private lateinit var imageMenu: ImageView
    private lateinit var drawerLayout: DrawerLayout
    private lateinit var btnBack: Button
    private lateinit var chatNickname: TextView
    private lateinit var currentUserId: String
    private lateinit var currentUserName: String
    private lateinit var targetUserId: String
    private lateinit var targetUserName: String
    private lateinit var webSocketManager: WebSocketManager
    private lateinit var chatRoomIdd: String

    private val chatRoomViewModel: ChatRoomViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)

        targetUserId = intent.getStringExtra("targetUserId") ?: "Unknown User"
        targetUserName = intent.getStringExtra("targetUserName") ?: "Unknown User"
        val chatRoomIdString = intent.getStringExtra("chatRoomId") ?: "-1"
        val chatRoomId = chatRoomIdString.toIntOrNull() ?: -1

        chatRoomIdd = chatRoomIdString

        val sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE)
        currentUserId = sharedPreferences.getString("UserID", "defaultUserId") ?: "defaultUserId"
        currentUserName = sharedPreferences.getString("userName", "defaultUserName") ?: "defaultUserName"

        initializeComponents()
        setupButtonListeners()

        adapter = ChatAdapter(currentUserId, listOf(), ::onAcceptClick, ::onRejectClick)
        recyclerView.adapter = adapter
        recyclerView.layoutManager = LinearLayoutManager(this)

        chatRoomViewModel.chatMessages.observe(this, Observer<List<ChatMessage>> { messages ->
            Log.d("ChatActivity", "Observed messages: $messages")
            adapter.submitList(messages)
            recyclerView.scrollToPosition(messages.size - 1)
        })

        chatRoomViewModel.errorMessage.observe(this, Observer { errorMessage ->
            if (errorMessage.isNotEmpty()) {
                Toast.makeText(this, errorMessage, Toast.LENGTH_LONG).show()
            }
        })

        webSocketManager = WebSocketManager(
            chatRoomId = chatRoomId,
            onMessageReceived = { messages: List<ChatMessage> -> runOnUiThread {
                Log.d("ChatActivity", "Received messages: $messages")
                chatRoomViewModel.addMessages(messages)
            }},
            onConnectionFailed = { error: String -> runOnUiThread {
                Toast.makeText(this, "WebSocket 연결 실패: $error", Toast.LENGTH_LONG).show()
                Log.e("ChatActivity", "웹소켓 연결 실패: $error")
            }}
        )

        webSocketManager.connect()
    }

    private fun initializeComponents() {
        messageInput = findViewById(R.id.chat_input)
        sendButton = findViewById(R.id.message_send)
        recyclerView = findViewById(R.id.chat_recyclerView)
        imageMenu = findViewById(R.id.imageMenu)
        drawerLayout = findViewById(R.id.drawerLayout)
        btnBack = findViewById(R.id.btn_back)
        chatNickname = findViewById(R.id.chat_nickname)

        chatNickname.text = targetUserName
    }

    private fun setupButtonListeners() {
        sendButton.setOnClickListener {
            val text = messageInput.text.toString()
            if (text.isNotEmpty()) {
                sendMessage(text)
                messageInput.text.clear()
            } else {
                Toast.makeText(this, "메시지를 입력하세요", Toast.LENGTH_SHORT).show()
            }
        }

        btnBack.setOnClickListener {
            finish()
        }

        imageMenu.setOnClickListener {
            val popupMenu = PopupMenu(this, imageMenu)
            popupMenu.inflate(R.menu.chat_menu)
            popupMenu.setOnMenuItemClickListener { item: MenuItem ->
                when (item.itemId) {
                    R.id.matching_user -> {
                        val intent = Intent(this, MatchmakingActivity::class.java)
                        intent.putExtra("targetUserId", targetUserId)
                        intent.putExtra("currentUserId", currentUserId)
                        startActivity(intent)
                        true
                    }
                    R.id.action_report -> {
                        val intent = Intent(this, ReportUserActivity::class.java)
                        intent.putExtra("targetUserId", targetUserId)
                        startActivity(intent)
                        true
                    }
                    R.id.action_block -> {
                        val intent = Intent(this, BlockUserActivity::class.java)
                        intent.putExtra("targetUserId", targetUserId)
                        startActivity(intent)
                        true
                    }
                    else -> false
                }
            }
            popupMenu.show()
        }
    }

    private fun sendMessage(messageText: String) {
        val messageData = ChatMessage(
            CHistoryID = chatRoomIdd, // 서버에서 생성
            senderID = currentUserId,
            receiverID = targetUserId,
            content = messageText
        )

        val jsonObject = JSONObject().apply {
            put("CHistoryID", messageData.CHistoryID)
            put("senderID", messageData.senderID)
            put("receiverID", messageData.receiverID)
            put("content", messageData.content)
        }

        webSocketManager.sendMessage(jsonObject.toString())
    }

    // 수락 버튼 클릭 이벤트 처리 메서드
    private fun onAcceptClick(chatMessage: ChatMessage) {
        val matchRequest = MatchRequest(userId = currentUserId, userId2 = targetUserId)

        KiriServicePool.matchingService.acceptMatch(matchRequest).enqueue(object :
            Callback<MatchResponse> {
            override fun onResponse(call: Call<MatchResponse>, response: Response<MatchResponse>) {
                if (response.isSuccessful) {
                    response.body()?.let {
                        if (it.success) {
                            sendMatchAcceptedMessage(chatMessage)
                        } else {
                            showError("매칭 수락에 실패했습니다")
                        }
                    }
                } else {
                    showError("매칭 수락에 실패했습니다.")
                }
            }

            override fun onFailure(call: Call<MatchResponse>, t: Throwable) {
                showError("네트워크 오류: ${t.message}")
            }
        })
    }

    // 매칭 수락 메시지 전송 메서드
    private fun sendMatchAcceptedMessage(chatMessage: ChatMessage) {
        val messageData = ChatMessage(
            CHistoryID = "", // 서버에서 생성
            senderID = currentUserId,
            receiverID = chatMessage.senderID,
            content = "매칭 요청이 수락되었습니다.",
            isMatchRequest = false // 일반 메시지로 전환
        )

        val jsonObject = JSONObject().apply {
            put("CHistoryID", messageData.CHistoryID)
            put("senderID", messageData.senderID)
            put("receiverID", messageData.receiverID)
            put("content", messageData.content)
            put("isMatchRequest", messageData.isMatchRequest)
        }

        webSocketManager.sendMessage(jsonObject.toString())
    }

    // 거절 버튼 클릭 이벤트 처리 메서드
    private fun onRejectClick(chatMessage: ChatMessage) {
        val matchRequest = MatchRequest(userId = currentUserId,
                    userId2 = targetUserId)

        KiriServicePool.matchingService.rejectMatch(matchRequest).enqueue(object : Callback<MatchResponse> {
            override fun onResponse(call: Call<MatchResponse>, response: Response<MatchResponse>) {
                if (response.isSuccessful) {
                    response.body()?.let {
                        if (it.success) {
                            sendMatchRejectedMessage(chatMessage)
                        } else {
                            showError("매칭 거절에 실패했습니다.")
                        }
                    }
                } else {
                    showError("매칭 거절에 실패했습니다.")
                }
            }

            override fun onFailure(call: Call<MatchResponse>, t: Throwable) {
                showError("네트워크 오류: ${t.message}")
            }
        })
    }

    // 매칭 거절 메시지 전송 메서드
    private fun sendMatchRejectedMessage(chatMessage: ChatMessage) {
        val messageData = ChatMessage(
            CHistoryID = "", // 서버에서 생성
            senderID = currentUserId,
            receiverID = chatMessage.senderID,
            content = "매칭 요청이 거절되었습니다.",
            isMatchRequest = false // 일반 메시지로 전환
        )

        val jsonObject = JSONObject().apply {
            put("CHistoryID", messageData.CHistoryID)
            put("senderID", messageData.senderID)
            put("receiverID", messageData.receiverID)
            put("content", messageData.content)
            put("isMatchRequest", messageData.isMatchRequest)
        }

        webSocketManager.sendMessage(jsonObject.toString())
    }

    //추가: 오류 메시지 표시 메서드
    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    override fun onDestroy() {
        super.onDestroy()
        webSocketManager.disconnect()
    }



}