
<template>
    <span>
        <home-hero></home-hero>
	<user-profile></user-profile>
    </span>
</template>

<script>
import HomeHero from '@/components/HomeHero';
import UserProfile from '@/components/UserProfile';

export default {
    name: 'home',
    components: {
        HomeHero,
	UserProfile,
    }
};
</script>
