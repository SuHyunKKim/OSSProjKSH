package com.example.mytestapp.mypage

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView // TextView import 추가
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentTransaction
import com.example.mytestapp.BlockListActivity
import com.example.mytestapp.R
import com.example.mytestapp.profile.ProfileOption1Activity
import com.example.mytestapp.sign.LoginActivity
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.example.mytestapp.HomeFragment
import com.example.mytestapp.match.MatchingFragment

class MyPageFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.fragment_mypage, container, false)

        // SharedPreferences에서 저장된 아이디 불러오기
        val sharedPreferences = requireContext().getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        val userID = sharedPreferences.getString("UserID", "")

        // 아이디를 표시할 TextView를 찾음
        val idTextView = view.findViewById<TextView>(R.id.ID)

        // 아이디 설정
        idTextView.text = userID // 로그인 액티비티에서 저장한 아이디로 설정


        // 프로필 수정 버튼 클릭 시
        view.findViewById<Button>(R.id.editProfileButton).setOnClickListener {
            // TODO: 프로필 수정 버튼 클릭 시 동작 구현
            // ProfileOption1Activity로 이동
            val intent = Intent(requireContext(), ProfileOption1Activity::class.java)
            startActivity(intent)
        }

//        // 차단 목록 관리 버튼 클릭 시
//        view.findViewById<Button>(R.id.blockListButton).setOnClickListener {
//            // TODO: 차단 목록 관리 버튼 클릭 시 동작 구현
//            // 차단 목록 액티비티를 열거나 프래그먼트 내에서 차단 목록을 관리하는 기능
//            val intent = Intent(requireContext(), BlockListActivity::class.java)
//            startActivity(intent)
//        }

        // 로그아웃 버튼 클릭 시
        view.findViewById<Button>(R.id.logout).setOnClickListener {
            // 로그아웃 실행
            logout()
        }

        // 하단 네비게이션뷰 설정
        val bottomNavigationView = view.findViewById<BottomNavigationView>(R.id.bnv_main)
        bottomNavigationView.setOnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_home -> {
                    // 홈 프래그먼트로 전환
                    replaceFragment(HomeFragment())
                    true
                }
                R.id.nav_roomate -> {
                    // 매칭 프래그먼트로 전환
                    replaceFragment(MatchingFragment())
                    true
                }
                R.id.nav_chat -> {
                    // 채팅 히스토리 프래그먼트로 전환
                    replaceFragment(MatchingFragment())
                    true
                }
                R.id.nav_mypage -> {
                    // 이미 마이페이지 프래그먼트에 있으므로 아무 작업 필요하지 않음
                    true
                }
                else -> false
            }
        }

        return view
    }

    // Fragment를 전환하는 함수
    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = requireFragmentManager().beginTransaction()
        transaction.replace(R.id.fragment_container, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }

    private fun logout() {
        // SharedPreferences에서 로그인 상태 초기화
        val sharedPreferences = requireContext().getSharedPreferences("MyPrefs", Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.clear()
        editor.apply()

        // 로그인 화면으로 이동
        val intent = Intent(requireContext(), LoginActivity::class.java)
        startActivity(intent)
        requireActivity().finish() // 현재 액티비티 종료
    }
}
