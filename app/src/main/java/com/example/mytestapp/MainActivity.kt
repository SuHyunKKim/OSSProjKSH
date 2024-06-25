package com.example.mytestapp

import com.example.mytestapp.mypage.MyPageFragment
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.fragment.app.Fragment
import com.example.mytestapp.databinding.ActivityMainBinding
import com.example.mytestapp.match.MatchingFragment

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    private lateinit var userID: String
    private lateinit var userName: String
    private lateinit var userStudentID: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // 로그인 화면에서 전달된 사용자 정보를 저장
        userID = intent.getStringExtra("userid") ?: "unknownID"
        userName = intent.getStringExtra("username") ?: "unknownName"
        userStudentID = intent.getStringExtra("studentid") ?: "unknownStudentID"

        // SharedPreferences에 사용자 정보 저장
        val sharedPreferences = getSharedPreferences("MyPrefs", MODE_PRIVATE)
        with(sharedPreferences.edit()) {
            putString("userId", userID)
            putString("userName", userName)
            putString("userStudentId", userStudentID)
            apply()
        }

        // 기본 프래그먼트 설정
        replaceFragment(HomeFragment())

        // 하단 네비게이션 설정
        binding.bnvMain.setOnNavigationItemSelectedListener { item ->
            when(item.itemId) {
                R.id.nav_home -> {
                    replaceFragment(HomeFragment())
                    true
                }
                R.id.nav_roomate -> {
                    replaceFragment(MatchingFragment())
                    true
                }
                R.id.nav_chat -> {
                    replaceFragment(MatchingFragment())
                    true
                }
                R.id.nav_mypage -> {
                    navigateToMyPageFragment()
                    true
                }
                else -> false
            }
        }
    }

    private fun navigateToMyPageFragment() {
        // MyPageFragment 인스턴스 생성
        val myPageFragment = MyPageFragment()

        // MyPageFragment로 전환
        replaceFragment(myPageFragment)
    }

    private fun replaceFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction().replace(R.id.main_container, fragment).commit()
    }
}
