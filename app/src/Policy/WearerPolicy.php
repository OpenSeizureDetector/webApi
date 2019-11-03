<?php
namespace App\Policy;

use App\Model\Entity\Wearer;
use Authorization\IdentityInterface;

class WearerPolicy
{
    const USERTYPE_ADMIN = 1;
    const USERTYPE_ANALYST = 2;

    public function canCreate(IdentityInterface $user, Wearer $wearer)
    {
        // Admin can create a wearer for any user.
        // A user can only create a wearer for that user.
        $allowed = false;
        // only admin can create users
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        if ($wearer->user_id == $user->id)
            $allowed = true;
        return $allowed;

    }

    public function canUpdate(IdentityInterface $user, Wearer $wearer)
    {
        return $this->canCreate($user, $wearer);
    }

    public function canEdit(IdentityInterface $user, Wearer $wearer) {
        return $this->canCreate($user, $wearer);
    }
    
    public function canDelete(IdentityInterface $user, Wearer $wearer)
    {
        echo("canDelete() - user=".$user->id.". ");
        return $this->canCreate($user, $wearer);
    }

    public function canView(IdentityInterface $user, Wearer $wearer)
    {
        $allowed = false;
        if ($user->usertype_id == self::USERTYPE_ADMIN)
            $allowed = true;
        if ($user->id == $wearer->user_id)
            $allowed = true;
        return $allowed;
    }
}
