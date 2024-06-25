package com.example.mytestapp.adapters

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.mytestapp.databinding.ChatMessageItemBinding
import com.example.mytestapp.databinding.ChatMessageItemMatchRequestBinding
import com.example.mytestapp.model.response.ChatMessage

class ChatAdapter(
    private val currentUserId: String,
    private var messages: List<ChatMessage>,
    private val onAcceptClick: (ChatMessage) -> Unit,
    private val onRejectClick: (ChatMessage) -> Unit
) : RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    companion object {
        private const val VIEW_TYPE_MESSAGE = 1
        private const val VIEW_TYPE_MATCH_REQUEST = 2
    }

    // 채팅 메시지를 위한 뷰홀더 클래스
    inner class ChatViewHolder(private val binding: ChatMessageItemBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            binding.chatMessage = message
            binding.executePendingBindings()

            if (message.senderID == currentUserId) {
                binding.layoutSentMessage.visibility = View.VISIBLE
                binding.layoutReceivedMessage.visibility = View.GONE
            } else {
                binding.layoutReceivedMessage.visibility = View.VISIBLE
                binding.layoutSentMessage.visibility = View.GONE
            }
        }
    }

    // 매칭 요청 메시지를 위한 뷰홀더 클래스
    inner class MatchRequestViewHolder(private val binding: ChatMessageItemMatchRequestBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            binding.executePendingBindings()

            binding.acceptButton.setOnClickListener { onAcceptClick(message) }
            binding.rejectButton.setOnClickListener { onRejectClick(message) }
        }
    }

    // 각 메시지의 뷰 타입을 반환하는 함수
    override fun getItemViewType(position: Int): Int {
        return if (messages[position].isMatchRequest) {
            VIEW_TYPE_MATCH_REQUEST
        } else {
            VIEW_TYPE_MESSAGE
        }
    }

    // 뷰홀더를 생성하는 함수
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        val layoutInflater = LayoutInflater.from(parent.context)
        return when (viewType) {
            VIEW_TYPE_MATCH_REQUEST -> {
                val binding = ChatMessageItemMatchRequestBinding.inflate(layoutInflater, parent, false)
                MatchRequestViewHolder(binding)
            }
            VIEW_TYPE_MESSAGE -> {
                val binding = ChatMessageItemBinding.inflate(layoutInflater, parent, false)
                ChatViewHolder(binding)
            }
            else -> throw IllegalArgumentException("Invalid view type")
        }
    }

    // 뷰홀더에 데이터를 바인딩하는 함수
    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        when (holder.itemViewType) {
            VIEW_TYPE_MATCH_REQUEST -> (holder as MatchRequestViewHolder).bind(messages[position])
            VIEW_TYPE_MESSAGE -> (holder as ChatViewHolder).bind(messages[position])
        }
    }

    // 아이템의 총 개수를 반환하는 함수
    override fun getItemCount(): Int = messages.size

    // 새로운 메시지 리스트를 설정하고 갱신하는 함수
    fun submitList(newMessages: List<ChatMessage>) {
        messages = newMessages
        notifyDataSetChanged()
    }
}
