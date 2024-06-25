package com.example.mytestapp.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.mytestapp.model.response.ChatMessage
// 채팅 메시지를 관리하고 UI와 데이터 소스를 연결
class ChatRoomViewModel : ViewModel() {
    private val _chatMessages = MutableLiveData<List<ChatMessage>>()
    val chatMessages: LiveData<List<ChatMessage>> get() = _chatMessages

    private val _errorMessage = MutableLiveData<String>()
    val errorMessage: LiveData<String> get() = _errorMessage

    // loadMessages 메서드는 더 이상 필요하지 않음
    // fun loadMessages(currentUserId: String, targetUserId: String) {
    //     // 서버에서 메시지를 불러와서 _chatMessages에 설정하는 로직
    //     // 예: _chatMessages.value = fetchedMessages
    // }

    fun addMessage(message: ChatMessage) {
        val updatedMessages = _chatMessages.value.orEmpty().toMutableList()
        updatedMessages.add(message)
        _chatMessages.value = updatedMessages
    }

    fun addMessages(messages: List<ChatMessage>) {
        val updatedMessages = _chatMessages.value.orEmpty().toMutableList()
        updatedMessages.addAll(messages)
        _chatMessages.value = updatedMessages
    }

    fun setError(message: String) {
        _errorMessage.value = message
    }
}