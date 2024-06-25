package com.example.mytestapp.matchmaking
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.mytestapp.R
import com.example.mytestapp.entitiy.KiriServicePool
import com.example.mytestapp.model.request.MatchRequest
import com.example.mytestapp.model.response.MatchResponse
import com.example.mytestapp.websocket.WebSocketManager
import org.json.JSONObject
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
class MatchmakingActivity : AppCompatActivity() {
    private var targetUserId: String = ""
    private var currentUserId: String = ""
    private lateinit var webSocketManager: WebSocketManager
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat_confirmation)
        // 인텐트에서 전달된 사용자 ID를 가져옴
        targetUserId = intent.getStringExtra("targetUserId") ?: ""
        currentUserId = intent.getStringExtra("currentUserId") ?: ""
        if (targetUserId.isNotEmpty()) {
            updateUI(targetUserId) // 사용자 ID가 유효한 경우 사용자 이름을 조회하지 않고 바로 업데이트
        } else {
            showError("사용자 ID를 가져올 수 없습니다.") // 사용자 ID가 유효하지 않은 경우 에러 메시지 표시
        }
        // WebSocketManager 초기화 및 연결
        webSocketManager = WebSocketManager(
            chatRoomId = null,
            onMessageReceived = { /* 메시지 수신 처리 */ },
            onConnectionFailed = { error -> runOnUiThread {
                Toast.makeText(this, "WebSocket 연결 실패: $error", Toast.LENGTH_LONG).show() // 수정
                Log.e("MatchmakingAc", "웹소켓 연결 실패: $error")
            }}
        )
        webSocketManager.connect()
        val confirmButton = findViewById<Button>(R.id.confirm_button)
        val cancelButton = findViewById<Button>(R.id.cancel_button)
        confirmButton.setOnClickListener {
            performMatching() // 매칭을 수행하는 메서드 호출
        }
        cancelButton.setOnClickListener {
            finish()  // 액티비티 종료
        }
    }
    // 조회한 사용자 이름으로 UI를 업데이트
    private fun updateUI(userName: String) {
        val confirmationMessage = findViewById<TextView>(R.id.confirmation_message)
        confirmationMessage.text = "$userName 사용자와 매칭을 진행하시겠습니까?"
    }
    // 에러 메시지를 토스트로 표시하는 메서드
    private fun showError(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
    // 매칭을 수행하는 메서드
    private fun performMatching() {
        // 현재 사용자의 ID를 포함하는 매칭 요청 객체 생성
        val matchRequest = MatchRequest(
            userId = currentUserId,
            userId2 = targetUserId
        )
        // 매칭 요청을 서버에 보냄
        KiriServicePool.matchingService.requestMatch(matchRequest).enqueue(object : Callback<MatchResponse> {
            override fun onResponse(call: Call<MatchResponse>, response: Response<MatchResponse>) {
                if (response.isSuccessful) {
                    val matchResponse = response.body()
                    if (matchResponse?.success == true) {
                        findViewById<TextView>(R.id.confirmation_message).text = "해당 사용자에게 매칭을 신청했습니다. 상대가 매칭을 수락하면 매칭이 완료됩니다."
                        sendMatchRequestToTarget()
                    } else {
                        Log.e("MatchmakingActivity", "매칭 신청에 실패했습니다. : 1")
                        Toast.makeText(this@MatchmakingActivity, "매칭 신청에 실패했습니다.", Toast.LENGTH_SHORT).show()
//                        showError(matchResponse?.message ?: "매칭 신청에 실패했습니다.")
                    }
                } else {
                    Log.e("MatchmakingActivity", "매칭 신청에 실패했습니다. : 2")
                    Toast.makeText(this@MatchmakingActivity, "매칭 신청에 실패했습니다.", Toast.LENGTH_SHORT).show()
                }
            }
            override fun onFailure(call: Call<MatchResponse>, t: Throwable) {
                showError("네트워크 오류: ${t.message}")
            }
        })
    }
    private fun sendMatchRequestToTarget() {
        val messageData = JSONObject().apply {
            put("type", "match_request")
            put("senderId", currentUserId)
            put("receiverId", targetUserId)
            put("content", "상대가 매칭을 신청했습니다. 매칭을 수락하시겠습니까?\n")
        }
        webSocketManager.sendMessage(messageData.toString())
    }
    override fun onDestroy() {
        super.onDestroy()
        webSocketManager.disconnect()
    }
}