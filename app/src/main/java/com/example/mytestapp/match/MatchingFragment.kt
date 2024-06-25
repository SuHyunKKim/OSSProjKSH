package com.example.mytestapp.match

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.mytestapp.databinding.FragmentMatchingBinding
import com.google.android.material.bottomnavigation.BottomNavigationView
import com.example.mytestapp.viewmodel.MatchingViewModel
import com.example.mytestapp.adapter.MatchingAdapter
import androidx.fragment.app.FragmentTransaction
import com.example.mytestapp.HomeFragment
import com.example.mytestapp.mypage.MyPageFragment
import com.example.mytestapp.R

class MatchingFragment : Fragment() {
    private var _binding: FragmentMatchingBinding? = null
    private val binding get() = _binding!!
    private lateinit var viewModel: MatchingViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentMatchingBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        viewModel = ViewModelProvider(this).get(MatchingViewModel::class.java)
        binding.lifecycleOwner = viewLifecycleOwner
        binding.viewModel = viewModel
        val adapter = MatchingAdapter(viewModel)
        binding.rvMatchingList.adapter = adapter
        binding.rvMatchingList.layoutManager = LinearLayoutManager(context)

        // 데이터를 로드
        viewModel.loadMatchingProfiles(requireContext())

        // 수정: ViewModel에서 제공하는 리스트 데이터를 어댑터에 전달
        viewModel.matchingProfiles.observe(viewLifecycleOwner) { profiles ->
            profiles?.let { adapter.submitList(it) }
        }

        binding.imageMenu.setOnClickListener {
            viewModel.onMenuButtonClicked(it)
        }

        // 하단 네비게이션뷰 설정
        val bottomNavigationView =
            binding.root.findViewById<BottomNavigationView>(R.id.bnv_main)
        // 매칭 프래그먼트가 선택되도록 기본으로 설정
        bottomNavigationView.selectedItemId = R.id.nav_roomate
        bottomNavigationView.setOnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.nav_home -> {
                    // 홈 프래그먼트로 전환
                    replaceFragment(HomeFragment())
                    true
                }

                R.id.nav_roomate -> {
                    // 이미 매칭 프래그먼트에 있으므로 아무 작업 필요하지 않음
                    true
                }

                R.id.nav_chat -> {
                    // 채팅 히스토리 프래그먼트로 전환
                    replaceFragment(MatchingFragment())
                    true
                }

                R.id.nav_mypage -> {
                    // 마이페이지 프래그먼트로 전환
                    replaceFragment(MyPageFragment())
                    true
                }

                else -> {
                    true // 이미 선택된 아이템이므로 아무 작업도 수행하지 않음
                }
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    // Fragment를 전환하는 함수
    private fun replaceFragment(fragment: Fragment) {
        val transaction: FragmentTransaction = requireFragmentManager().beginTransaction()
        transaction.replace(R.id.fragment_container, fragment)
        transaction.addToBackStack(null)
        transaction.commit()
    }
}
