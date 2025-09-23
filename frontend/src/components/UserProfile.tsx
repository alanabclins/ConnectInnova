// 'use client'

// import { useEffect, useState } from 'react'
// import { useForm } from 'react-hook-form'
// import type { SubmitHandler } from 'react-hook-form'
// import { useNavigate } from 'react-router'
// import { toast } from 'sonner'
// import { Avatar } from '@/components/ui/avatar'
// import { Button } from '@/components/ui/button'
// import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
// import { Dialog, DialogContent, DialogHeader, DialogFooter } from '@/components/ui/dialog'
// import { Input } from '@/components/ui/input'
// import { Label } from '@/components/ui/label'
// import { Checkbox } from '@/components/ui/checkbox'
// import type { User } from '../../app/models/user'
// import { useAuth } from '../../src/context/auth'
// import userService from '../../app/services/user.service'
// import { IconBrandGoogle } from '@tabler/icons-react'

// interface UserProfileProps {
//   userProfile: User
//   onUserUpdated?: (user: User) => void
//   allowDelete: boolean
// }

// export default function UserProfile({ userProfile, onUserUpdated, allowDelete }: UserProfileProps) {
//   const navigate = useNavigate()
//   const { user: currentUser, setUser, logout } = useAuth()
//   const [open, setOpen] = useState(false)

//   const {
//     register,
//     handleSubmit,
//     reset,
//     formState: { errors },
//   } = useForm<User>({
//     defaultValues: userProfile,
//   })

//   useEffect(() => {
//     reset(userProfile)
//   }, [userProfile, reset])

//   const onSubmit: SubmitHandler<User> = async (data) => {
//     try {
//       let updatedUser: User
//       if (currentUser?.uuid === userProfile.uuid) {
//         updatedUser = await userService.updateProfile(data)
//         setUser(updatedUser)
//       } else {
//         updatedUser = await userService.updateUser(userProfile.uuid, data)
//       }
//       toast.success('User profile updated successfully.')
//       onUserUpdated?.(updatedUser)
//     } catch (error: any) {
//       const msg = error?.response?.data?.detail ?? error?.message ?? 'Failed to update user.'
//       toast.error(msg)
//     }
//   }

//   const handleDeleteProfile = () => setOpen(true)
//   const handleCancel = () => setOpen(false)

//   const handleConfirm = async () => {
//     setOpen(false)
//     try {
//       await userService.deleteSelf()
//       toast.success('Your account has been deleted.')
//       logout()
//       navigate('/')
//     } catch {
//       toast.error('Failed to delete account.')
//     }
//   }

//   return (
//     <Card className='max-w-lg mx-auto'>
//       <CardHeader>
//         <CardTitle>User Profile</CardTitle>
//       </CardHeader>
//       <CardContent className='flex flex-col items-center'>
//         <label className='cursor-pointer'>
//           <input type='file' className='hidden' accept='image/*' />
//           <Avatar className='w-14 h-14 mb-4'>
//             {(!userProfile.picture && userProfile.first_name?.[0]) || ''}
//           </Avatar>
//         </label>

//         <form
//           onSubmit={handleSubmit(onSubmit)}
//           className='w-full flex flex-col gap-4'
//           key={userProfile.uuid}
//           data-testid='user-profile-form'
//         >
//           <div className='grid grid-cols-1 sm:grid-cols-2 gap-4'>
//             <div>
//               <Label htmlFor='first_name'>First Name</Label>
//               <Input id='first_name' {...register('first_name')} />
//             </div>
//             <div>
//               <Label htmlFor='last_name'>Last Name</Label>
//               <Input id='last_name' {...register('last_name')} />
//             </div>
//           </div>

//           <div>
//             <Label htmlFor='email'>Email</Label>
//             <Input
//               id='email'
//               {...register('email', { required: true })}
//               disabled={!!userProfile.provider}
//             />
//             {errors.email && (
//               <p className='text-red-500 text-sm'>Please provide an email address.</p>
//             )}
//           </div>

//           {userProfile.provider && (
//             <div className='relative'>
//               <IconBrandGoogle
//                 className='absolute left-3 top-1/2 -translate-y-1/2 text-gray-500'
//                 size={20}
//               />
//               <Input
//                 id='provider'
//                 value={userProfile.provider}
//                 disabled
//                 className='pl-10' // espaço para o ícone
//               />
//             </div>
//           )}

//           {!userProfile.provider && (
//             <div>
//               <Label htmlFor='password'>Password</Label>
//               <Input id='password' type='password' {...register('password')} />
//             </div>
//           )}

//           {currentUser?.is_superuser && (
//             <>
//               <div className='flex items-center gap-2'>
//                 <Checkbox
//                   {...register('is_active')}
//                   disabled={currentUser.uuid === userProfile.uuid}
//                   defaultChecked={userProfile.is_active}
//                 />
//                 <span>Is Active</span>
//               </div>
//               <div className='flex items-center gap-2'>
//                 <Checkbox
//                   {...register('is_superuser')}
//                   disabled={currentUser.uuid === userProfile.uuid}
//                   defaultChecked={userProfile.is_superuser}
//                 />
//                 <span>Is Super User</span>
//               </div>
//             </>
//           )}

//           <Button type='submit' className='mt-2 w-full'>
//             Update
//           </Button>

//           {allowDelete && (
//             <Button variant='destructive' className='mt-2 w-full' onClick={handleDeleteProfile}>
//               Delete my account
//             </Button>
//           )}
//         </form>
//       </CardContent>

//       <Dialog open={open} onOpenChange={setOpen}>
//         <DialogContent>
//           <DialogHeader>
//             <CardTitle>Confirm Deletion</CardTitle>
//           </DialogHeader>
//           <p>Are you sure you want to delete your account?</p>
//           <DialogFooter className='flex justify-end gap-2 mt-2'>
//             <Button variant='outline' onClick={handleCancel}>
//               Cancel
//             </Button>
//             <Button variant='destructive' onClick={handleConfirm}>
//               Confirm
//             </Button>
//           </DialogFooter>
//         </DialogContent>
//       </Dialog>
//     </Card>
//   )
// }
